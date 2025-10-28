import curses
from .screen_base import ScreenBase
from .menu import ListSelector
from src.models import Flight
from datetime import datetime, timedelta


class FlightsScreen(ScreenBase):
    """Screen for viewing flights and routes"""

    def display(self):
        """Display flights screen"""
        while True:
            self.clear()
            self.draw_header("VIEW FLIGHTS & ROUTES")

            # Display date filter options
            self.stdscr.attron(curses.color_pair(3))
            self.stdscr.addstr(4, 5, "Select date to view flights:")
            self.stdscr.attroff(curses.color_pair(3))

            today = datetime.now()
            dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
            dates.append("ALL")

            y_pos = 6
            for idx, date in enumerate(dates):
                label = date if date != "ALL" else "View All Flights"
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y_pos + idx, 7, f"{idx + 1}. {label}")
                self.stdscr.attroff(curses.color_pair(1))

            self.draw_footer("1-8: Select date | ESC: Back")
            self.refresh()

            key = self.stdscr.getch()

            if key == 27:  # ESC
                return
            elif ord('1') <= key <= ord('8'):
                idx = key - ord('1')
                if idx < len(dates):
                    date_filter = None if dates[idx] == "ALL" else dates[idx]
                    self.show_flights(date_filter)

    def show_flights(self, date_filter=None):
        """Show list of flights"""
        flights = Flight.get_all(date_filter)

        if not flights:
            self.show_message("No flights found for this date")
            return

        def format_flight(flight):
            return f"{flight.flight_number} | {flight.flight_date} {flight.departure_time} | {flight.origin_code}->{flight.dest_code} | {Flight.get_available_seats(flight.id)}/{flight.capacity} seats"

        while True:
            self.clear()
            self.draw_header("FLIGHT LIST")

            if date_filter:
                self.stdscr.attron(curses.color_pair(3))
                self.stdscr.addstr(3, 5, f"Date: {date_filter}")
                self.stdscr.attroff(curses.color_pair(3))

            # Display flights
            start_y = 5
            max_visible = self.height - 12
            visible_flights = flights[:max_visible]

            self.stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            self.stdscr.addstr(start_y - 1, 5, "FLIGHT | DATE       TIME  | ROUTE    | SEATS AVAIL")
            self.stdscr.addstr(start_y, 5, "-" * 60)
            self.stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

            for idx, flight in enumerate(visible_flights):
                y_pos = start_y + 1 + idx
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y_pos, 5, format_flight(flight)[:self.width-10])
                self.stdscr.attroff(curses.color_pair(1))

            if len(flights) > max_visible:
                self.stdscr.attron(curses.color_pair(5))
                self.stdscr.addstr(self.height - 5, 5, f"Showing {max_visible} of {len(flights)} flights")
                self.stdscr.attroff(curses.color_pair(5))

            self.draw_footer("ESC: Back")
            self.refresh()

            key = self.stdscr.getch()
            if key == 27:  # ESC
                return
