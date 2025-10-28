# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

KidAirlines is a retro airline reservation system designed for children's play. It simulates 1980s/90s terminal-based reservation systems with keyboard and arrow key navigation.

**Technology Stack:**
- Python 3.6+ (uses standard library only, no external dependencies)
- SQLite (local database - `kidairlines.db`)
- Python curses library (built-in terminal UI framework)

**Design Philosophy:**
- Zero external dependencies for easy deployment
- Retro aesthetic (1980s/90s green-screen terminal)
- Educational focus - simple, readable code
- All interactions through keyboard (no mouse)

## Development Commands

### Running the Application
```bash
python3 main.py
```
First run automatically initializes database with sample data.

### Resetting the Database
```bash
rm kidairlines.db && python3 main.py
```
Useful for testing with fresh data.

### Database Initialization Only
```bash
python3 src/database/db_init.py
```
Creates/resets database without starting the UI.

### Quick Database Test
```python
# Create a test script to verify models
import sys, os
sys.path.insert(0, 'src')
from src.models import Airport, Flight, Reservation

print(f"Airports: {len(Airport.get_all())}")
print(f"Flights: {len(Flight.get_all())}")
print(f"Reservations: {len(Reservation.get_all())}")
```

## Project Architecture

### Directory Structure
```
kidairlines/
├── main.py                          # Application entry point
├── kidairlines.db                   # SQLite database (created on first run)
├── kidairlines.md                   # Original requirements
├── README.md                        # User documentation
├── CLAUDE.md                        # This file - developer guide
├── requirements.txt                 # Empty (no dependencies needed)
├── .gitignore                       # Git ignore rules
└── src/
    ├── __init__.py
    ├── database/
    │   ├── __init__.py
    │   ├── schema.sql               # Complete database schema
    │   └── db_init.py               # Database setup and seeding
    ├── models/                      # Data access layer
    │   ├── __init__.py
    │   ├── database.py              # Connection manager & query helpers
    │   ├── airport.py               # Airport model
    │   ├── route.py                 # Route model
    │   ├── flight.py                # Flight model
    │   ├── passenger.py             # Passenger model
    │   └── reservation.py           # Reservation model
    └── ui/                          # Terminal UI layer
        ├── __init__.py
        ├── screen_base.py           # Base screen class with common UI utilities
        ├── menu.py                  # Menu and ListSelector components
        ├── flights_screen.py        # View flights & routes
        ├── booking_screen.py        # Book tickets
        ├── reservations_screen.py   # View passenger reservations
        ├── manifest_screen.py       # View flight passenger manifests
        ├── config_screen.py         # Manage airports & routes
        └── manage_reservations_screen.py  # Cancel/reactivate reservations
```

### Layer Architecture

**1. Database Layer** (`src/database/`)

File: `schema.sql`
- Complete SQLite schema with tables, indexes, foreign keys
- Self-documenting with clear naming conventions
- Includes constraints to maintain data integrity

File: `db_init.py`
- `init_database()`: Creates tables from schema.sql, seeds data if empty
- `seed_data()`: Creates hub-and-spoke network centered on EWR with 12 airports, 22 routes, flights for next 7 days, passengers, reservations
- `get_db_path()`: Returns path to database file (project_root/kidairlines.db)
- Network design: EWR (Newark) as central hub with routes to 11 domestic and international destinations
- Flight scheduling: Uses realistic flight durations and schedules based on actual distances
- `route_schedules` dictionary: Maps route_id to list of (departure_time, duration_minutes, capacity) tuples
- `calculate_arrival_time()`: Helper function to compute arrival time from departure + duration, handles next-day arrivals

**2. Models Layer** (`src/models/`)

File: `database.py` - Core database utilities
- `get_db_connection()`: Context manager for database connections
- `execute_query(query, params)`: Execute SELECT queries, returns list of Row objects
- `execute_update(query, params)`: Execute INSERT/UPDATE/DELETE, returns lastrowid

Model Files: `airport.py`, `route.py`, `flight.py`, `passenger.py`, `reservation.py`
- Each model represents one database table
- All methods are static (models are not instantiated)
- Models use `__init__` to hold row data as attributes
- Common pattern: `get_all()`, `get_by_id()`, `create()`, `update()`, `delete()`
- Models include JOIN queries to fetch related data (e.g., Route includes airport codes)

**3. UI Layer** (`src/ui/`)

File: `screen_base.py` - Base class for all screens
- `ScreenBase`: Abstract base providing common UI utilities
- `setup_colors()`: Initializes 5 color pairs for retro look
- `draw_header(title)`: Draws top bar with app title
- `draw_footer(instructions)`: Draws bottom bar with key hints
- `draw_box()`: Draws ASCII box with optional title
- `show_message()`: Modal message box (waits for keypress)
- `get_input()`: Text input prompt with echo/cursor handling
- `display()`: Abstract method - override in subclasses

File: `menu.py` - Reusable menu components
- `Menu`: Vertical menu with arrow key navigation
  - Takes list of tuples: `(display_text, callback_function)`
  - Callbacks return "EXIT" to close menu, None to continue
- `ListSelector`: Scrollable list picker
  - Takes list of items and optional display_func
  - Returns selected item or None on cancel
  - Handles long lists with scroll indicators

Feature Screens: `*_screen.py`
- Each extends `ScreenBase` and implements `display()`
- Self-contained - handle all user interaction within the screen
- Return to caller when user presses ESC or completes action
- Use composition of Menu/ListSelector for complex interactions

### Database Schema

**airports**
```sql
id, code (unique), name, city, active (0/1)
```
- Represents airports in the system
- `active` flag allows disabling without deletion

**routes**
```sql
id, origin_airport_id, destination_airport_id, flight_number (unique)
```
- Represents flight routes between two airports
- `flight_number` is the identifier (e.g., "KA101")
- One-way only (need two routes for round-trip)

**flights**
```sql
id, route_id, departure_time, arrival_time, flight_date, capacity
```
- Specific scheduled instances of routes
- One route can have many flights on different dates/times
- `capacity` is total seats (default 150)

**passengers**
```sql
id, first_name, last_name, date_of_birth, created_at
```
- Represents individual passengers
- `date_of_birth` is optional

**reservations**
```sql
id, passenger_id, confirmation_number (unique), created_at, status
```
- Booking records for passengers
- `confirmation_number`: 6-char alphanumeric (e.g., "V6EM0L")
- `status`: "CONFIRMED" or "CANCELLED"
- One passenger can have multiple reservations

**reservation_flights**
```sql
id, reservation_id, flight_id, seat_number
```
- Many-to-many link between reservations and flights
- Allows multi-leg trips (one reservation, multiple flights)
- `seat_number`: Optional seat assignment (e.g., "12A")
- Unique constraint on (flight_id, seat_number) prevents double-booking

**Key Relationships & Constraints:**
- Route requires two different airports (origin != destination)
- Flight must reference valid route
- Reservation must reference valid passenger
- Reservation_flight must reference valid reservation AND flight
- Seat numbers are unique per flight
- Indexes on date, passenger_id, reservation_id for query performance

### Data Flow Patterns

**Booking a Ticket (booking_screen.py):**
1. Select/create passenger → `Passenger.create()` or select from `Passenger.get_all()`
2. Select flight date → Display date options
3. Select flight → `Flight.get_all(date_filter)`, filter by availability
4. Enter seat number → User input
5. Create reservation → `Reservation.create(passenger_id)` generates confirmation
6. Link flight to reservation → `Reservation.add_flight(reservation_id, flight_id, seat)`

**Viewing Itinerary (reservations_screen.py):**
1. Lookup by confirmation → `Reservation.get_by_confirmation(conf_number)`
2. Get reservation flights → `reservation.get_flights()` (JOIN query)
3. Display formatted itinerary with all flight details

**Configuration Changes (config_screen.py):**
1. List current items → `Airport.get_all(active_only=False)` or `Route.get_all()`
2. User selects action (add/toggle/delete)
3. Get input or show selector
4. Execute model method → `Airport.create()`, `Route.delete()`, etc.
5. Refresh display to show changes

### UI Patterns & Conventions

**Color Pairs (curses):**
```python
curses.color_pair(1)  # Green on black - main text
curses.color_pair(2)  # Yellow on black - instructions/highlighted
curses.color_pair(3)  # Cyan on black - headers/titles
curses.color_pair(4)  # Black on green - selected menu items
curses.color_pair(5)  # Red on black - errors/warnings
```

**Navigation Keys:**
- Arrow Up/Down: Navigate menus and lists
- ENTER: Select/confirm current item
- ESC (key code 27): Go back/cancel
- Q: Quit (main menu only)
- Letter keys: Action shortcuts (e.g., 'A' for Add, 'D' for Delete)
- Number keys: Quick selection in some menus

**Common UI Patterns:**

1. **Menu Pattern:**
```python
options = [
    ("Option 1", self.callback1),
    ("Option 2", self.callback2),
    ("Exit", lambda: "EXIT")
]
menu = Menu(self.stdscr, "TITLE", options)
menu.display()
```

2. **List Selection Pattern:**
```python
items = Model.get_all()
selector = ListSelector(
    self.stdscr,
    "SELECT ITEM",
    items,
    lambda item: f"{item.name} ({item.id})"  # Display formatter
)
selected = selector.display()  # Returns item or None
```

3. **Input Pattern:**
```python
value = self.get_input("Prompt:", y, x, max_length)
if not value:
    return  # User cancelled or entered nothing
```

4. **Message Pattern:**
```python
self.show_message("Operation successful!")
self.show_message("Error occurred", error=True)  # Red text
```

**Screen Lifecycle:**
```python
class MyScreen(ScreenBase):
    def display(self):
        while True:  # Loop for screen re-rendering
            self.clear()
            self.draw_header("SCREEN TITLE")

            # Draw content here

            self.draw_footer("Instructions")
            self.refresh()

            key = self.stdscr.getch()

            if key == 27:  # ESC
                return  # Exit screen
            elif key == ord('a'):
                self.some_action()
```

### Code Conventions

**Python Style:**
- Use snake_case for functions and variables
- Use PascalCase for class names
- Static methods for all model operations
- Docstrings on public methods
- Type hints not used (Python 3.6 compatibility)

**Database Conventions:**
- Table names: plural, lowercase (e.g., `flights`)
- Column names: snake_case (e.g., `first_name`)
- Foreign keys: `table_id` pattern (e.g., `passenger_id`)
- Always use parameterized queries (never string interpolation)
- Use `execute_query()` for reads, `execute_update()` for writes

**UI Conventions:**
- All screens extend `ScreenBase`
- Use `self.stdscr` for curses operations
- Always call `self.clear()` before redrawing
- Always call `self.refresh()` after drawing
- Use `curses.curs_set(0)` to hide cursor (except during input)
- Handle ESC (key code 27) for "go back"
- Y coordinate first, X coordinate second: `addstr(y, x, text)`

### Common Maintenance Tasks

**Adding a New Airport:**
1. Use Configuration screen in the app, OR
2. Direct SQL: `INSERT INTO airports (code, name, city, active) VALUES ('XXX', 'Airport Name', 'City', 1);`

**Adding Sample Flights:**
Modify `route_schedules` dictionary in `seed_data()` in `src/database/db_init.py`:
```python
route_schedules = {
    # Format: route_id: [(departure_time, duration_in_minutes, capacity), ...]
    1: [('06:00', 120, 150), ('12:00', 120, 150)],  # EWR->DTW (2h)
    # Add more routes...
}
```

**Flight Time Calculation:**
The system automatically calculates arrival times based on departure time and duration:
- Duration specified in minutes for precision
- Handles next-day arrivals (e.g., overnight international flights)
- Accounts for different aircraft capacities by route type
- Short-haul routes get more frequent service (3-4 flights/day)
- Long-haul routes typically have 1-2 flights/day

**Changing Color Scheme:**
Modify `setup_colors()` in `src/ui/screen_base.py`:
```python
curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Change from green to blue
```

**Adding a New Screen:**
1. Create `src/ui/my_feature_screen.py`:
```python
from .screen_base import ScreenBase

class MyFeatureScreen(ScreenBase):
    def display(self):
        self.clear()
        self.draw_header("MY FEATURE")
        # ... implementation ...
        self.refresh()
```

2. Import in `main.py`:
```python
from src.ui.my_feature_screen import MyFeatureScreen
```

3. Add to menu options in `KidAirlinesApp.run()`:
```python
menu_options = [
    # ... existing options ...
    ("My Feature", self.my_feature),
]

def my_feature(self):
    screen = MyFeatureScreen(self.stdscr)
    screen.display()
    return None
```

**Adding a Database Field:**
1. Modify `src/database/schema.sql` (add column to table)
2. Delete `kidairlines.db`
3. Run `python3 main.py` to recreate with new schema
4. Update corresponding model in `src/models/` to handle new field

### Testing Strategies

**Manual Testing:**
```bash
# Start fresh
rm kidairlines.db && python3 main.py

# Test workflow:
# 1. Book a ticket (creates passenger, reservation)
# 2. View reservations for that passenger
# 3. View itinerary by confirmation number
# 4. View manifest to see passenger on flight
# 5. Cancel reservation
# 6. Verify status changed
```

**Database Verification:**
```bash
# If sqlite3 is available:
sqlite3 kidairlines.db "SELECT COUNT(*) FROM flights;"

# Using Python:
python3 -c "import sys; sys.path.insert(0, 'src'); from src.models import Flight; print(len(Flight.get_all()))"
```

**Model Testing:**
```python
# Create test_models.py
import sys, os
sys.path.insert(0, 'src')
from src.models import Passenger, Reservation

# Test create
pid = Passenger.create("Test", "User", "2010-01-01")
print(f"Created passenger {pid}")

# Test retrieve
p = Passenger.get_by_id(pid)
print(f"Retrieved: {p.full_name()}")

# Test reservation
rid, conf = Reservation.create(pid)
print(f"Created reservation {conf}")
```

### Known Limitations & Gotchas

1. **Curses Limitations:**
   - Requires terminal with at least 80x24 characters
   - Colors may not work on all terminals
   - Does NOT work on Windows without third-party curses (use WSL)
   - Text input limited to single line

2. **Database:**
   - No migration system - schema changes require database reset
   - No foreign key cascade deletes (must manually handle)
   - Deleting routes affects all flights on that route (warn user)
   - No authentication/multi-user support

3. **UI Limitations:**
   - No search functionality (must scroll through lists)
   - Lists show max ~10-20 items (scroll for more)
   - No confirmation number validation (assumes uppercase alphanumeric)
   - Date format hardcoded as YYYY-MM-DD

4. **Business Logic:**
   - No seat map display (seats are just text input)
   - No seat availability check before assignment (relies on unique constraint)
   - Flight times don't account for time zones
   - No ticket pricing
   - Reservations can't be edited (must cancel and recreate)

5. **Error Handling:**
   - Database errors show generic message (not user-friendly)
   - Network errors N/A (local only)
   - Invalid input may crash (e.g., non-numeric where expected)

### Troubleshooting

**Problem: Application won't start / curses error**
- Solution: Ensure terminal supports curses. On Windows, use WSL or install windows-curses
- Check: `python3 -c "import curses; print('OK')"`

**Problem: Database corruption / weird data**
- Solution: Delete database and restart: `rm kidairlines.db && python3 main.py`

**Problem: Colors not showing correctly**
- Solution: Check terminal supports colors: `echo $TERM` (should be xterm-256color or similar)
- Try: `export TERM=xterm-256color` before running

**Problem: Can't see cursor during input**
- Solution: This is intentional. Cursor appears as underscore characters (_____) at input position

**Problem: Screen is garbled**
- Solution: Terminal too small. Resize to at least 80x24. Check with: `tput cols; tput lines`

**Problem: Key presses not working**
- Solution: Ensure `keypad(True)` is set in main.py (it is by default)
- Some terminals may not support all keys (especially ESC on macOS)

**Problem: Import errors**
- Solution: Ensure running from project root directory
- Check: Python path includes 'src' directory (main.py does this automatically)

### Extension Ideas

**Potential Enhancements:**

1. **Search Functionality:**
   - Add `Passenger.search(name)` (already implemented)
   - Add search screen to find passengers by partial name
   - Add flight search by route or flight number

2. **Reporting:**
   - Most popular routes (count reservations per route)
   - Revenue reports (if pricing added)
   - Occupancy rates by flight/date

3. **Advanced Booking:**
   - Multi-leg trip booking (already supported in data model)
   - Round-trip booking helper
   - Seat map visualization (ASCII art of plane)

4. **Data Management:**
   - Export reservations to CSV
   - Import airports/routes from file
   - Backup/restore database

5. **UI Improvements:**
   - Pagination controls (Page Up/Down)
   - Better date picker (calendar view)
   - Help screen with key commands
   - Confirmation prompts for destructive actions

6. **Business Features:**
   - Ticket pricing and payment tracking
   - Frequent flyer program
   - Boarding pass printing (ASCII art)
   - Standby list for full flights

### File Reference Guide

**When you need to...**

- **Modify database schema**: Edit `src/database/schema.sql`
- **Change sample data**: Edit `seed_data()` in `src/database/db_init.py`
- **Add database query logic**: Add to relevant model in `src/models/`
- **Change UI colors**: Edit `setup_colors()` in `src/ui/screen_base.py`
- **Add common UI utilities**: Add to `ScreenBase` in `src/ui/screen_base.py`
- **Create new menu**: Use `Menu` class from `src/ui/menu.py`
- **Create new list selector**: Use `ListSelector` from `src/ui/menu.py`
- **Add new feature screen**: Create new file in `src/ui/`, extend `ScreenBase`
- **Modify main menu**: Edit `run()` method in `main.py`
- **Change window setup**: Edit `setup_terminal()` in `main.py`

### Quick Reference: Model Methods

```python
# Airport
Airport.get_all(active_only=True)
Airport.get_by_id(airport_id)
Airport.get_by_code(code)
Airport.create(code, name, city)
Airport.update_status(airport_id, active)

# Route
Route.get_all()
Route.get_by_id(route_id)
Route.create(origin_airport_id, destination_airport_id, flight_number)
Route.delete(route_id)

# Flight
Flight.get_all(date_filter=None)
Flight.get_by_id(flight_id)
Flight.get_available_seats(flight_id)
Flight.create(route_id, departure_time, arrival_time, flight_date, capacity)

# Passenger
Passenger.get_all()
Passenger.get_by_id(passenger_id)
Passenger.search(search_term)
Passenger.create(first_name, last_name, date_of_birth)
Passenger.update(passenger_id, first_name, last_name, date_of_birth)

# Reservation
Reservation.get_all()
Reservation.get_by_id(reservation_id)
Reservation.get_by_confirmation(confirmation_number)
Reservation.get_by_passenger(passenger_id)
Reservation.create(passenger_id, confirmation_number=None)  # Returns (id, conf_num)
Reservation.update_status(reservation_id, status)
Reservation.delete(reservation_id)
Reservation.add_flight(reservation_id, flight_id, seat_number)
Reservation.remove_flight(reservation_id, flight_id)
reservation.get_flights()  # Instance method - returns list of flight dicts
```

### Dependencies & Compatibility

**Python Version:**
- Minimum: Python 3.6
- Tested on: Python 3.8+
- Works on: Linux, macOS, WSL

**External Dependencies:**
- None (uses only Python standard library)

**Terminal Requirements:**
- Minimum size: 80 columns x 24 rows (recommended: 100x30)
- Color support: Optional but recommended
- Supported terminals: xterm, gnome-terminal, iTerm2, Terminal.app, WSL terminal

**Platform Notes:**
- Linux/macOS: Native curses support, works out of box
- Windows: Requires WSL or `windows-curses` package
- Raspberry Pi: Fully supported

### Additional Resources

**Python curses documentation:**
- https://docs.python.org/3/howto/curses.html

**SQLite documentation:**
- https://www.sqlite.org/docs.html

**Testing curses apps:**
- Use `curses.wrapper()` for proper cleanup
- Errors will reset terminal automatically
- CTRL+C exits safely

**Debugging curses apps:**
```python
# Can't print() during curses - terminal is taken over
# Instead, write to a file:
with open('debug.log', 'a') as f:
    f.write(f"Debug: {some_variable}\n")
```
