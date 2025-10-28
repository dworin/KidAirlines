import curses
from .screen_base import ScreenBase
from .menu import ListSelector
from src.models import Passenger, Flight, Reservation
from datetime import datetime, timedelta


class BookingScreen(ScreenBase):
    """Screen for booking tickets"""

    def display(self):
        """Display booking screen"""
        self.clear()
        self.draw_header("BOOK TICKETS")
        self.draw_footer("Following prompts...")
        self.refresh()

        # Step 1: Select or create passenger
        passenger = self.select_passenger()
        if not passenger:
            return

        # Step 2: Select flight
        flight = self.select_flight()
        if not flight:
            return

        # Step 3: Get seat number
        seat = self.get_seat_number()
        if not seat:
            return

        # Step 4: Create reservation
        try:
            reservation_id, conf_number = Reservation.create(passenger.id)
            success = Reservation.add_flight(reservation_id, flight.id, seat)

            if success:
                self.show_message(f"Booking confirmed! Confirmation: {conf_number}")
            else:
                self.show_message("Booking failed - seat may be taken", error=True)
        except Exception as e:
            self.show_message(f"Booking failed: {str(e)}", error=True)

    def select_passenger(self):
        """Select or create a passenger"""
        self.clear()
        self.draw_header("SELECT PASSENGER")

        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(5, 5, "1. Select existing passenger")
        self.stdscr.addstr(6, 5, "2. Create new passenger")
        self.stdscr.addstr(7, 5, "3. Cancel")
        self.stdscr.attroff(curses.color_pair(1))

        self.draw_footer("1-3: Select option")
        self.refresh()

        key = self.stdscr.getch()

        if key == ord('1'):
            passengers = Passenger.get_all()
            if not passengers:
                self.show_message("No passengers found. Please create one.")
                return self.create_passenger()

            selector = ListSelector(
                self.stdscr,
                "SELECT PASSENGER",
                passengers,
                lambda p: f"{p.full_name()} (ID: {p.id})"
            )
            return selector.display()

        elif key == ord('2'):
            return self.create_passenger()

        return None

    def create_passenger(self):
        """Create a new passenger"""
        self.clear()
        self.draw_header("CREATE PASSENGER")
        self.refresh()

        first_name = self.get_input("First Name:", 5, 5, 30)
        if not first_name:
            return None

        last_name = self.get_input("Last Name:", 7, 5, 30)
        if not last_name:
            return None

        dob = self.get_input("Date of Birth (YYYY-MM-DD):", 9, 5, 10)

        passenger_id = Passenger.create(first_name, last_name, dob if dob else None)
        return Passenger.get_by_id(passenger_id)

    def select_flight(self):
        """Select a flight"""
        # Show next 7 days
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
            return None

        if ord('1') <= key <= ord('7'):
            idx = key - ord('1')
            date_filter = dates[idx]

            flights = Flight.get_all(date_filter)
            available_flights = [f for f in flights if Flight.get_available_seats(f.id) > 0]

            if not available_flights:
                self.show_message("No flights available for this date")
                return None

            selector = ListSelector(
                self.stdscr,
                f"SELECT FLIGHT - {date_filter}",
                available_flights,
                lambda f: f"{f.flight_number} {f.departure_time} {f.origin_code}->{f.dest_code} ({Flight.get_available_seats(f.id)} seats)"
            )
            return selector.display()

        return None

    def get_seat_number(self):
        """Get seat number from user"""
        self.clear()
        self.draw_header("ENTER SEAT NUMBER")
        self.refresh()

        seat = self.get_input("Seat (e.g., 12A):", 5, 5, 5)
        return seat.upper() if seat else None
