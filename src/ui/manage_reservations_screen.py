import curses
from .screen_base import ScreenBase
from .menu import ListSelector
from src.models import Reservation


class ManageReservationsScreen(ScreenBase):
    """Screen for managing reservations (edit, cancel)"""

    def display(self):
        """Display reservation management screen"""
        self.clear()
        self.draw_header("MANAGE RESERVATIONS")
        self.refresh()

        conf = self.get_input("Enter Confirmation Number:", 5, 5, 10)
        if not conf:
            return

        reservation = Reservation.get_by_confirmation(conf.upper())
        if not reservation:
            self.show_message("Reservation not found", error=True)
            return

        self.manage_reservation(reservation)

    def manage_reservation(self, reservation):
        """Manage a specific reservation"""
        while True:
            flights = reservation.get_flights()

            self.clear()
            self.draw_header("MANAGE RESERVATION")

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
            self.stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

            if not flights:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(start_y + 1, 7, "No flights in this reservation")
                self.stdscr.attroff(curses.color_pair(1))
            else:
                for idx, flight in enumerate(flights):
                    y_pos = start_y + 1 + idx
                    self.stdscr.attron(curses.color_pair(1))
                    display = f"{flight['flight_number']} | {flight['flight_date']} {flight['departure_time']} | {flight['origin_code']}->{flight['dest_code']} | Seat: {flight['seat_number']}"
                    self.stdscr.addstr(y_pos, 7, display[:self.width-12])
                    self.stdscr.attroff(curses.color_pair(1))

            # Options
            options_y = start_y + len(flights) + 3
            self.stdscr.attron(curses.color_pair(3))
            self.stdscr.addstr(options_y, 5, "Options:")
            self.stdscr.addstr(options_y + 1, 7, "C: Cancel Reservation")
            if reservation.status == "CANCELLED":
                self.stdscr.addstr(options_y + 2, 7, "R: Reactivate Reservation")
            self.stdscr.attroff(curses.color_pair(3))

            self.draw_footer("C: Cancel | R: Reactivate | ESC: Back")
            self.refresh()

            key = self.stdscr.getch()

            if key == 27:  # ESC
                return
            elif key in [ord('c'), ord('C')]:
                self.cancel_reservation(reservation)
            elif key in [ord('r'), ord('R')] and reservation.status == "CANCELLED":
                self.reactivate_reservation(reservation)

            # Refresh reservation data
            reservation = Reservation.get_by_id(reservation.id)

    def cancel_reservation(self, reservation):
        """Cancel a reservation"""
        if reservation.status == "CANCELLED":
            self.show_message("Reservation is already cancelled")
            return

        self.clear()
        self.draw_header("CANCEL RESERVATION")
        self.stdscr.attron(curses.color_pair(5))
        self.stdscr.addstr(5, 5, f"Cancel reservation {reservation.confirmation_number}?")
        self.stdscr.attroff(curses.color_pair(5))
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(7, 5, "Y: Confirm | N: Cancel")
        self.stdscr.attroff(curses.color_pair(1))
        self.refresh()

        confirm = self.stdscr.getch()
        if confirm in [ord('y'), ord('Y')]:
            try:
                Reservation.update_status(reservation.id, "CANCELLED")
                self.show_message("Reservation cancelled successfully")
            except Exception as e:
                self.show_message(f"Failed to cancel: {str(e)}", error=True)

    def reactivate_reservation(self, reservation):
        """Reactivate a cancelled reservation"""
        self.clear()
        self.draw_header("REACTIVATE RESERVATION")
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(5, 5, f"Reactivate reservation {reservation.confirmation_number}?")
        self.stdscr.addstr(7, 5, "Y: Confirm | N: Cancel")
        self.stdscr.attroff(curses.color_pair(1))
        self.refresh()

        confirm = self.stdscr.getch()
        if confirm in [ord('y'), ord('Y')]:
            try:
                Reservation.update_status(reservation.id, "CONFIRMED")
                self.show_message("Reservation reactivated successfully")
            except Exception as e:
                self.show_message(f"Failed to reactivate: {str(e)}", error=True)
