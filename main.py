#!/usr/bin/env python3
"""
KidAirlines - Retro Airline Reservation System
"""
import curses
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database import init_database
from src.ui.menu import Menu
from src.ui.flights_screen import FlightsScreen
from src.ui.booking_screen import BookingScreen
from src.ui.reservations_screen import ReservationsScreen, ItineraryScreen
from src.ui.manifest_screen import ManifestScreen
from src.ui.config_screen import ConfigScreen
from src.ui.manage_reservations_screen import ManageReservationsScreen


class KidAirlinesApp:
    """Main application class"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup_terminal()

    def setup_terminal(self):
        """Setup terminal for curses"""
        curses.curs_set(0)  # Hide cursor
        self.stdscr.keypad(True)  # Enable keypad mode

        # Initialize colors if available
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()

    def view_flights(self):
        """View flights and routes"""
        screen = FlightsScreen(self.stdscr)
        screen.display()
        return None

    def book_tickets(self):
        """Book tickets"""
        screen = BookingScreen(self.stdscr)
        screen.display()
        return None

    def view_reservations(self):
        """View passenger reservations"""
        screen = ReservationsScreen(self.stdscr)
        screen.display()
        return None

    def view_itinerary(self):
        """View itinerary"""
        screen = ItineraryScreen(self.stdscr)
        screen.display()
        return None

    def view_manifest(self):
        """View flight manifest"""
        screen = ManifestScreen(self.stdscr)
        screen.display()
        return None

    def configuration(self):
        """Configuration screen"""
        screen = ConfigScreen(self.stdscr)
        screen.display()
        return None

    def manage_reservations(self):
        """Manage reservations"""
        screen = ManageReservationsScreen(self.stdscr)
        screen.display()
        return None

    def exit_app(self):
        """Exit the application"""
        return "EXIT"

    def run(self):
        """Run the main application"""
        menu_options = [
            ("1. View Routes & Flights", self.view_flights),
            ("2. Book Tickets", self.book_tickets),
            ("3. View Passenger Reservations", self.view_reservations),
            ("4. View Itinerary", self.view_itinerary),
            ("5. View Flight Manifest", self.view_manifest),
            ("6. Configuration", self.configuration),
            ("7. Manage Reservations", self.manage_reservations),
            ("8. Exit", self.exit_app)
        ]

        menu = Menu(self.stdscr, "MAIN MENU", menu_options)
        menu.display()


def main(stdscr):
    """Main entry point"""
    app = KidAirlinesApp(stdscr)
    app.run()


if __name__ == '__main__':
    # Initialize database
    print("Initializing KidAirlines database...")
    init_database()
    print("Database ready!")
    print("Starting KidAirlines...")
    print()

    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
