import curses
from .screen_base import ScreenBase
from .menu import Menu, ListSelector
from src.models import Airport, Route


class ConfigScreen(ScreenBase):
    """Screen for configuring airports and routes"""

    def display(self):
        """Display configuration menu"""
        options = [
            ("Manage Airports", self.manage_airports),
            ("Manage Routes", self.manage_routes),
            ("Back to Main Menu", lambda: "EXIT")
        ]

        menu = Menu(self.stdscr, "CONFIGURATION", options)
        menu.display()

    def manage_airports(self):
        """Manage airports"""
        while True:
            airports = Airport.get_all(active_only=False)

            self.clear()
            self.draw_header("MANAGE AIRPORTS")

            start_y = 4
            self.stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            self.stdscr.addstr(start_y, 5, "CODE | AIRPORT NAME                          | CITY         | STATUS")
            self.stdscr.addstr(start_y + 1, 5, "-" * 75)
            self.stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

            max_visible = min(len(airports), self.height - start_y - 12)
            for idx, airport in enumerate(airports[:max_visible]):
                y_pos = start_y + 2 + idx
                status = "ACTIVE" if airport.active else "INACTIVE"
                color = curses.color_pair(1) if airport.active else curses.color_pair(5)

                self.stdscr.attron(color)
                display = f"{airport.code:4} | {airport.name:40} | {airport.city:12} | {status}"
                self.stdscr.addstr(y_pos, 5, display[:self.width-10])
                self.stdscr.attroff(color)

            self.stdscr.attron(curses.color_pair(3))
            self.stdscr.addstr(self.height - 6, 5, "Options:")
            self.stdscr.addstr(self.height - 5, 7, "A: Add Airport | T: Toggle Active Status")
            self.stdscr.attroff(curses.color_pair(3))

            self.draw_footer("A: Add | T: Toggle | ESC: Back")
            self.refresh()

            key = self.stdscr.getch()

            if key == 27:  # ESC
                return
            elif key in [ord('a'), ord('A')]:
                self.add_airport()
            elif key in [ord('t'), ord('T')]:
                self.toggle_airport_status(airports)

    def add_airport(self):
        """Add a new airport"""
        self.clear()
        self.draw_header("ADD AIRPORT")
        self.refresh()

        code = self.get_input("Airport Code (3 letters):", 5, 5, 3)
        if not code or len(code) != 3:
            self.show_message("Invalid airport code", error=True)
            return

        name = self.get_input("Airport Name:", 7, 5, 50)
        if not name:
            return

        city = self.get_input("City:", 9, 5, 30)
        if not city:
            return

        try:
            Airport.create(code.upper(), name, city)
            self.show_message(f"Airport {code.upper()} added successfully")
        except Exception as e:
            self.show_message(f"Failed to add airport: {str(e)}", error=True)

    def toggle_airport_status(self, airports):
        """Toggle airport active status"""
        selector = ListSelector(
            self.stdscr,
            "SELECT AIRPORT TO TOGGLE",
            airports,
            lambda a: f"{a.code} - {a.name} ({'ACTIVE' if a.active else 'INACTIVE'})"
        )
        airport = selector.display()

        if airport:
            new_status = 0 if airport.active else 1
            Airport.update_status(airport.id, new_status)
            status_text = "activated" if new_status else "deactivated"
            self.show_message(f"Airport {airport.code} {status_text}")

    def manage_routes(self):
        """Manage routes"""
        while True:
            routes = Route.get_all()

            self.clear()
            self.draw_header("MANAGE ROUTES")

            start_y = 4
            self.stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            self.stdscr.addstr(start_y, 5, "FLIGHT | ORIGIN -> DESTINATION")
            self.stdscr.addstr(start_y + 1, 5, "-" * 50)
            self.stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

            max_visible = min(len(routes), self.height - start_y - 12)
            for idx, route in enumerate(routes[:max_visible]):
                y_pos = start_y + 2 + idx

                self.stdscr.attron(curses.color_pair(1))
                display = f"{route.flight_number:6} | {route.origin_code} ({route.origin_city}) -> {route.dest_code} ({route.dest_city})"
                self.stdscr.addstr(y_pos, 5, display[:self.width-10])
                self.stdscr.attroff(curses.color_pair(1))

            self.stdscr.attron(curses.color_pair(3))
            self.stdscr.addstr(self.height - 6, 5, "Options:")
            self.stdscr.addstr(self.height - 5, 7, "A: Add Route | D: Delete Route")
            self.stdscr.attroff(curses.color_pair(3))

            self.draw_footer("A: Add | D: Delete | ESC: Back")
            self.refresh()

            key = self.stdscr.getch()

            if key == 27:  # ESC
                return
            elif key in [ord('a'), ord('A')]:
                self.add_route()
            elif key in [ord('d'), ord('D')]:
                self.delete_route(routes)

    def add_route(self):
        """Add a new route"""
        self.clear()
        self.draw_header("ADD ROUTE")
        self.refresh()

        # Select origin airport
        airports = Airport.get_all(active_only=True)
        if not airports:
            self.show_message("No airports available", error=True)
            return

        origin_selector = ListSelector(
            self.stdscr,
            "SELECT ORIGIN AIRPORT",
            airports,
            lambda a: f"{a.code} - {a.name}"
        )
        origin = origin_selector.display()
        if not origin:
            return

        # Select destination airport
        dest_airports = [a for a in airports if a.id != origin.id]
        dest_selector = ListSelector(
            self.stdscr,
            "SELECT DESTINATION AIRPORT",
            dest_airports,
            lambda a: f"{a.code} - {a.name}"
        )
        dest = dest_selector.display()
        if not dest:
            return

        # Get flight number
        self.clear()
        self.draw_header("ADD ROUTE")
        self.refresh()

        flight_number = self.get_input("Flight Number (e.g., KA123):", 5, 5, 10)
        if not flight_number:
            return

        try:
            Route.create(origin.id, dest.id, flight_number.upper())
            self.show_message(f"Route {flight_number.upper()} created: {origin.code} -> {dest.code}")
        except Exception as e:
            self.show_message(f"Failed to create route: {str(e)}", error=True)

    def delete_route(self, routes):
        """Delete a route"""
        if not routes:
            self.show_message("No routes available", error=True)
            return

        selector = ListSelector(
            self.stdscr,
            "SELECT ROUTE TO DELETE",
            routes,
            lambda r: f"{r.flight_number} | {r.origin_code} -> {r.dest_code}"
        )
        route = selector.display()

        if route:
            # Confirm deletion
            self.clear()
            self.draw_header("CONFIRM DELETION")
            self.stdscr.attron(curses.color_pair(5))
            self.stdscr.addstr(5, 5, f"Delete route {route.flight_number}?")
            self.stdscr.addstr(7, 5, "WARNING: This will affect all flights on this route!")
            self.stdscr.attroff(curses.color_pair(5))
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(9, 5, "Y: Confirm | N: Cancel")
            self.stdscr.attroff(curses.color_pair(1))
            self.refresh()

            confirm = self.stdscr.getch()
            if confirm in [ord('y'), ord('Y')]:
                try:
                    Route.delete(route.id)
                    self.show_message(f"Route {route.flight_number} deleted")
                except Exception as e:
                    self.show_message(f"Failed to delete route: {str(e)}", error=True)
