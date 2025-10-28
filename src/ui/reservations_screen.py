import curses
from .screen_base import ScreenBase
from .menu import ListSelector
from src.models import Passenger, Reservation


class ReservationsScreen(ScreenBase):
    """Screen for viewing passenger reservations"""

    def display(self):
        """Display reservations screen"""
        # Select passenger
        passengers = Passenger.get_all()
        if not passengers:
            self.show_message("No passengers found")
            return

        selector = ListSelector(
            self.stdscr,
            "SELECT PASSENGER",
            passengers,
            lambda p: f"{p.full_name()} (ID: {p.id})"
        )
        passenger = selector.display()

        if not passenger:
            return

        # Show reservations for selected passenger
        self.show_passenger_reservations(passenger)

    def show_passenger_reservations(self, passenger):
        """Show all reservations for a passenger"""
        reservations = Reservation.get_by_passenger(passenger.id)

        if not reservations:
            self.show_message(f"No reservations found for {passenger.full_name()}")
            return

        while True:
            self.clear()
            self.draw_header(f"RESERVATIONS - {passenger.full_name()}")

            start_y = 4
            self.stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            self.stdscr.addstr(start_y, 5, "CONFIRMATION | STATUS    | CREATED")
            self.stdscr.addstr(start_y + 1, 5, "-" * 50)
            self.stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

            for idx, res in enumerate(reservations[:15]):  # Show max 15
                y_pos = start_y + 2 + idx
                self.stdscr.attron(curses.color_pair(1))
                display = f"{res.confirmation_number} | {res.status:10} | {res.created_at or 'N/A'}"
                self.stdscr.addstr(y_pos, 5, display[:self.width-10])
                self.stdscr.attroff(curses.color_pair(1))

            self.stdscr.attron(curses.color_pair(3))
            self.stdscr.addstr(self.height - 6, 5, "Enter confirmation number to view itinerary")
            self.stdscr.attroff(curses.color_pair(3))

            self.draw_footer("ESC: Back")
            self.refresh()

            # Allow user to enter confirmation number
            conf = self.get_input("Confirmation:", self.height - 4, 5, 10)
            if conf:
                reservation = Reservation.get_by_confirmation(conf.upper())
                if reservation:
                    self.show_itinerary(reservation)
                else:
                    self.show_message("Reservation not found", error=True)
            else:
                return


class ItineraryScreen(ScreenBase):
    """Screen for viewing itinerary details"""

    def display(self):
        """Display itinerary lookup screen"""
        self.clear()
        self.draw_header("VIEW ITINERARY")
        self.refresh()

        conf = self.get_input("Enter Confirmation Number:", 5, 5, 10)
        if not conf:
            return

        reservation = Reservation.get_by_confirmation(conf.upper())
        if not reservation:
            self.show_message("Reservation not found", error=True)
            return

        self.show_itinerary(reservation)


def show_itinerary(self, reservation):
    """Show detailed itinerary for a reservation"""
    flights = reservation.get_flights()

    while True:
        self.clear()
        self.draw_header("ITINERARY")

        # Reservation details
        self.stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
        self.stdscr.addstr(3, 5, f"Confirmation: {reservation.confirmation_number}")
        self.stdscr.addstr(4, 5, f"Passenger: {reservation.passenger_name()}")
        self.stdscr.addstr(5, 5, f"Status: {reservation.status}")
        self.stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)

        # Flight details
        start_y = 7
        self.stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
        self.stdscr.addstr(start_y, 5, "FLIGHTS:")
        self.stdscr.addstr(start_y + 1, 5, "-" * 70)
        self.stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

        if not flights:
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(start_y + 2, 5, "No flights in this reservation")
            self.stdscr.attroff(curses.color_pair(1))
        else:
            for idx, flight in enumerate(flights):
                y_pos = start_y + 2 + idx * 3

                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y_pos, 7, f"Flight: {flight['flight_number']}")
                self.stdscr.addstr(y_pos + 1, 7,
                                 f"Route: {flight['origin_city']} ({flight['origin_code']}) -> "
                                 f"{flight['dest_city']} ({flight['dest_code']})")
                self.stdscr.addstr(y_pos + 2, 7,
                                 f"Date: {flight['flight_date']} | "
                                 f"Depart: {flight['departure_time']} | "
                                 f"Arrive: {flight['arrival_time']} | "
                                 f"Seat: {flight['seat_number'] or 'N/A'}")
                self.stdscr.attroff(curses.color_pair(1))

        self.draw_footer("ESC: Back")
        self.refresh()

        key = self.stdscr.getch()
        if key == 27:  # ESC
            return


# Add method to ReservationsScreen
ReservationsScreen.show_itinerary = show_itinerary
ItineraryScreen.show_itinerary = show_itinerary
