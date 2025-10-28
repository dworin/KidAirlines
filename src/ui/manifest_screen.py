import curses
from .screen_base import ScreenBase
from .menu import ListSelector
from src.models import Flight
from src.models.database import execute_query
from datetime import datetime, timedelta


class ManifestScreen(ScreenBase):
    """Screen for viewing flight manifests (passenger lists)"""

    def display(self):
        """Display manifest screen"""
        # Select date
        today = datetime.now()
        dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

        self.clear()
        self.draw_header("SELECT FLIGHT DATE")

        for idx, date in enumerate(dates):
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(5 + idx, 5, f"{idx + 1}. {date}")
            self.stdscr.attroff(curses.color_pair(1))

        self.draw_footer("1-7: Select date | ESC: Cancel")
        self.refresh()

        key = self.stdscr.getch()
        if key == 27:
            return

        if ord('1') <= key <= ord('7'):
            idx = key - ord('1')
            date_filter = dates[idx]

            flights = Flight.get_all(date_filter)
            if not flights:
                self.show_message("No flights for this date")
                return

            selector = ListSelector(
                self.stdscr,
                f"SELECT FLIGHT - {date_filter}",
                flights,
                lambda f: f"{f.flight_number} {f.departure_time} {f.origin_code}->{f.dest_code}"
            )
            flight = selector.display()

            if flight:
                self.show_manifest(flight)

    def show_manifest(self, flight):
        """Show passenger manifest for a flight"""
        # Get passengers on this flight
        query = """
            SELECT p.first_name, p.last_name, rf.seat_number, r.confirmation_number
            FROM reservation_flights rf
            JOIN reservations r ON rf.reservation_id = r.id
            JOIN passengers p ON r.passenger_id = p.id
            WHERE rf.flight_id = ?
            ORDER BY rf.seat_number
        """
        passengers = execute_query(query, (flight.id,))

        while True:
            self.clear()
            self.draw_header("FLIGHT MANIFEST")

            # Flight details
            self.stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
            self.stdscr.addstr(3, 5, f"Flight: {flight.flight_number}")
            self.stdscr.addstr(4, 5, f"Route: {flight.origin_code} -> {flight.dest_code}")
            self.stdscr.addstr(5, 5, f"Date: {flight.flight_date} | Departure: {flight.departure_time}")
            self.stdscr.addstr(6, 5, f"Passengers: {len(passengers)} / {flight.capacity}")
            self.stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)

            # Passenger list
            start_y = 8
            self.stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            self.stdscr.addstr(start_y, 5, "SEAT | PASSENGER NAME           | CONFIRMATION")
            self.stdscr.addstr(start_y + 1, 5, "-" * 60)
            self.stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

            if not passengers:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(start_y + 2, 5, "No passengers booked on this flight")
                self.stdscr.attroff(curses.color_pair(1))
            else:
                max_visible = min(len(passengers), self.height - start_y - 7)
                for idx, passenger in enumerate(passengers[:max_visible]):
                    y_pos = start_y + 2 + idx
                    seat = passenger['seat_number'] or 'N/A'
                    name = f"{passenger['first_name']} {passenger['last_name']}"
                    conf = passenger['confirmation_number']

                    self.stdscr.attron(curses.color_pair(1))
                    display = f"{seat:4} | {name:25} | {conf}"
                    self.stdscr.addstr(y_pos, 5, display[:self.width-10])
                    self.stdscr.attroff(curses.color_pair(1))

                if len(passengers) > max_visible:
                    self.stdscr.attron(curses.color_pair(5))
                    self.stdscr.addstr(self.height - 5, 5, f"Showing {max_visible} of {len(passengers)} passengers")
                    self.stdscr.attroff(curses.color_pair(5))

            self.draw_footer("ESC: Back")
            self.refresh()

            key = self.stdscr.getch()
            if key == 27:  # ESC
                return
