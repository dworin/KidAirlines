<div align="center">

# ✈️ KidAirlines

### *Retro Terminal-Based Airline Reservation System*

**Experience the nostalgia of 1980s/90s green-screen airline terminals**

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-green.svg)](requirements.txt)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20wsl-lightgrey.svg)]()
[![License](https://img.shields.io/badge/license-Educational-orange.svg)]()

[Features](#-features) • [Screenshots](#️-screenshots) • [Quick Start](#-quick-start) • [Usage](#-how-to-use) • [Sample Data](#-sample-data) • [Developer Docs](CLAUDE.md)

---

</div>

## 📖 About

KidAirlines is a fully functional airline reservation system designed for children's play and education. Built with Python's curses library, it recreates the authentic look and feel of 1980s/90s terminal-based reservation systems used by travel agents and airline staff.

**Perfect for:**
- 🎮 Kids who love airplanes and travel
- 🎓 Learning about databases and reservation systems
- 💻 Experiencing retro computing interfaces
- 🏫 Educational projects and demonstrations
- 👨‍💻 Python programming tutorials

**Key Highlights:**
- Zero external dependencies - runs with standard Python
- Authentic retro green-screen aesthetic
- Complete reservation system with real database
- Keyboard-only navigation (no mouse needed)
- Hub-and-spoke airline network with realistic flight times

## 🖼️ Screenshots

### Main Menu
The classic green-on-black terminal interface with numbered menu options:

```
╔════════════════════════════════════════════════════════════════════════════╗
║                           KIDAIRLINES SYSTEM                               ║
╚════════════════════════════════════════════════════════════════════════════╝

                        > 1. View Routes & Flights <
                          2. Book Tickets
                          3. View Passenger Reservations
                          4. View Itinerary
                          5. View Flight Manifest
                          6. Configuration
                          7. Manage Reservations
                          8. Exit
```

### Flight Listing
Browse available flights with real-time seat availability:

```
╔════════════════════════════════════════════════════════════════════════════╗
║                         AVAILABLE FLIGHTS                                  ║
╚════════════════════════════════════════════════════════════════════════════╝

> KA101 | EWR → DTW | 06:00 → 08:00 | 2025-10-26 | Seats: 142/150
  KA102 | DTW → EWR | 09:30 → 11:30 | 2025-10-26 | Seats: 138/150
  KA103 | EWR → ORD | 07:00 → 09:15 | 2025-10-26 | Seats: 145/150
  KA201 | EWR → LHR | 22:00 → 05:00 | 2025-10-26 | Seats: 218/250
```

### Booking Confirmation
Instant confirmation codes for all reservations:

```
╔════════════════════════════════════════════════════════════════════════════╗
║                     BOOKING CONFIRMATION                                   ║
╚════════════════════════════════════════════════════════════════════════════╝

  Confirmation Number: V6EM0L
  Passenger: Emily Johnson
  Flight: KA101 (EWR → DTW)
  Date: 2025-10-26
  Departure: 06:00
  Arrival: 08:00
  Seat: 12A
  Status: CONFIRMED
```

## ✨ Features

### Core Functionality

1. **View Routes & Flights** 📋
   - Browse available flights by date
   - See seat availability in real-time
   - View next 7 days of scheduled flights
   - Filter by specific dates

2. **Book Tickets** 🎫
   - Create new passengers or select existing ones
   - Choose from available flights
   - Assign seat numbers
   - Receive confirmation codes

3. **View Passenger Reservations** 👤
   - Look up all reservations for any passenger
   - See confirmation numbers and status
   - Quick access to detailed itineraries

4. **View Itinerary** 📄
   - Look up reservations by confirmation number
   - See complete flight details
   - View route information and seat assignments

5. **View Flight Manifest** 📝
   - Display passenger lists for specific flights
   - See seat assignments
   - Check flight capacity and booking status

6. **Configuration** ⚙️
   - Manage airports (add new, enable/disable existing)
   - Create and delete flight routes
   - Full control over the airline network

7. **Manage Reservations** 🔧
   - Cancel reservations
   - Reactivate cancelled bookings
   - Update reservation status

## 🚀 Quick Start

### Prerequisites

| Requirement | Details |
|------------|---------|
| **Python** | Version 3.6 or higher |
| **Curses** | Built-in with Python on Unix/Linux/macOS |
| **Terminal** | Minimum 80×24 characters (100×30 recommended) |
| **Platform** | Linux, macOS, WSL, or Raspberry Pi |

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/kidairlines.git
cd kidairlines

# Run the application (no installation needed!)
python3 main.py
```

**That's it!** 🎉 The first run automatically creates and seeds the database with sample data.

### First Run

When you start KidAirlines for the first time, it will:
1. ✅ Create `kidairlines.db` SQLite database
2. ✅ Set up all tables and relationships
3. ✅ Seed with 12 airports and 22 routes
4. ✅ Generate 378 flights over the next 7 days
5. ✅ Create 15 sample passengers and 5 reservations
6. ✅ Launch the main menu

## 🎮 How to Use

### Main Menu Preview

```
╔════════════════════════════════════════════════════════════════════════════╗
║                           KIDAIRLINES SYSTEM                               ║
╚════════════════════════════════════════════════════════════════════════════╝

                        > 1. View Routes & Flights <
                          2. Book Tickets
                          3. View Passenger Reservations
                          4. View Itinerary
                          5. View Flight Manifest
                          6. Configuration
                          7. Manage Reservations
                          8. Exit

╔════════════════════════════════════════════════════════════════════════════╗
║     ↑/↓: Navigate | 1-9: Select | ENTER: Select | Q: Quit               ║
╚════════════════════════════════════════════════════════════════════════════╝
```

### Navigation Controls

| Key | Action |
|-----|--------|
| **↑/↓** (Arrow Keys) | Navigate menus and lists |
| **ENTER** | Select/confirm current item |
| **1-9** | Quick select menu option by number |
| **ESC** | Go back to previous screen |
| **Q** | Quit (from main menu) |
| **A/D/T** | Action shortcuts (varies by screen) |

### Example Workflow: Booking a Flight

1. Start the application
2. Select "2. Book Tickets" from main menu
3. Choose to create a new passenger or select existing
4. Pick a flight date (shows next 7 days)
5. Select an available flight
6. Enter a seat number (e.g., "12A")
7. Receive your confirmation number!

### Example Workflow: Checking an Itinerary

1. Select "4. View Itinerary" from main menu
2. Enter your confirmation number (e.g., "V6EM0L")
3. See complete flight details, routes, and seat assignment

### Configuration

Want to add your own airports or routes?

1. Select "6. Configuration" from main menu
2. Choose "Manage Airports" or "Manage Routes"
3. Follow the on-screen prompts to add or modify

## 📊 Sample Data

The application includes pre-loaded sample data with a **hub-and-spoke network** centered on Newark Liberty International (EWR):

### Airports (12 destinations)

**Hub:**
- **EWR** - Newark Liberty International

**Domestic Destinations:**
- **DTW** - Detroit Metropolitan Wayne County
- **ORD** - Chicago O'Hare
- **PBI** - West Palm Beach (Palm Beach International)
- **BWI** - Baltimore/Washington International
- **MIA** - Miami International
- **SFO** - San Francisco International
- **OMA** - Omaha (Eppley Airfield)

**International Destinations:**
- **DPS** - Bali (Ngurah Rai International)
- **CAI** - Cairo International
- **CDG** - Paris (Charles de Gaulle)
- **LHR** - London Heathrow

### Routes & Flights
- Hub-and-spoke network with EWR as the central hub
- 22 routes (11 from EWR to destinations, 11 return routes)
- 378 scheduled flights over the next 7 days (54 flights per day)
- **Realistic flight times** based on actual distances:
  - Short-haul domestic: 1-3 hours (e.g., EWR-BWI: 1h, EWR-MIA: 3h)
  - Cross-country: 5-6 hours (e.g., EWR-SFO: 6h 10m)
  - Transatlantic: 7-8 hours (e.g., EWR-LHR: 7h, EWR-CDG: 7.5h)
  - Long-haul international: 11-19 hours (e.g., EWR-CAI: 11h, EWR-Bali: 19h)
- Multiple daily frequencies on popular routes (up to 4 flights/day on short routes)
- Aircraft capacity varies by route: 120-250 seats
- Overnight international departures arrive next morning

### Passengers & Reservations
- 15 sample passengers
- 5 existing reservations to explore

## 🗄️ Database

All data is stored in `kidairlines.db` (SQLite database) in the project root.

### Resetting the Database

Want to start fresh with new sample data?

```bash
rm kidairlines.db
python3 main.py
```

The database will be automatically recreated with fresh sample data.

## 🖥️ System Requirements

### Supported Platforms
- ✅ Linux (all distributions)
- ✅ macOS
- ✅ Windows via WSL (Windows Subsystem for Linux)
- ✅ Raspberry Pi
- ❌ Native Windows (requires `windows-curses` package)

### Terminal Requirements
- Minimum size: 80 columns × 24 rows
- Recommended: 100 columns × 30 rows
- Color support recommended (but not required)

### Tested Terminals
- GNOME Terminal
- iTerm2
- Terminal.app (macOS)
- xterm
- WSL Terminal

## 🎨 Retro Aesthetic

KidAirlines recreates the authentic look and feel of 1980s-90s airline reservation systems:

- **Green-on-black color scheme** (classic terminal look)
- **ASCII box drawing** characters
- **Keyboard-only navigation** (no mouse needed!)
- **Text-based interface** with simple, clear layouts
- **Status indicators** and confirmation codes

## 🛠️ Technical Details

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    UI Layer (Curses)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │  Flights │ │ Booking  │ │  Itinerary│ │  Config  │  │
│  │  Screen  │ │  Screen  │ │   Screen  │ │  Screen  │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│                    Models Layer                         │
│  ┌──────────┐ ┌──────────┐ ┌────────────┐ ┌─────────┐ │
│  │ Airport  │ │  Route   │ │   Flight   │ │Passenger│ │
│  └──────────┘ └──────────┘ └────────────┘ └─────────┘ │
│  ┌──────────────────────────────────────────────────┐  │
│  │           Reservation (with flights)             │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│              Database Layer (SQLite)                    │
│  • airports  • routes  • flights  • passengers          │
│  • reservations  • reservation_flights                  │
└─────────────────────────────────────────────────────────┘
```

### Design Principles

- **Zero Dependencies**: Only Python standard library
- **3-Layer Architecture**: Clear separation (UI → Models → Database)
- **MVC Pattern**: Models handle business logic, Views handle display
- **SQLite Database**: Local storage, no server setup required
- **Curses UI**: Native terminal interface, works anywhere

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.6+ | Core application logic |
| **Database** | SQLite3 | Local data persistence |
| **UI Framework** | Python curses | Terminal-based interface |
| **Data Models** | Custom ORM-like layer | Database abstraction |

## 📁 Project Structure

```
kidairlines/
├── main.py                                 # 🚀 Application entry point
├── kidairlines.db                          # 💾 SQLite database (auto-created)
├── README.md                               # 📖 This file - User guide
├── CLAUDE.md                               # 👨‍💻 Comprehensive developer documentation
├── requirements.txt                        # 📦 Empty - no dependencies!
└── src/
    ├── database/
    │   ├── schema.sql                      # 🗄️  Complete database schema
    │   └── db_init.py                      # 🌱 Database setup & seeding logic
    ├── models/                             # 📊 Data access layer
    │   ├── database.py                     # 🔌 Connection manager & query helpers
    │   ├── airport.py                      # ✈️  Airport model
    │   ├── route.py                        # 🛤️  Route model
    │   ├── flight.py                       # 🎫 Flight model
    │   ├── passenger.py                    # 👤 Passenger model
    │   └── reservation.py                  # 📝 Reservation model
    └── ui/                                 # 🖥️  Terminal UI layer
        ├── screen_base.py                  # 🎨 Base screen class with utilities
        ├── menu.py                         # 📋 Menu & ListSelector components
        ├── flights_screen.py               # 🔍 View flights & routes
        ├── booking_screen.py               # 🎫 Book tickets
        ├── reservations_screen.py          # 👤 View passenger reservations
        ├── manifest_screen.py              # 📃 View flight manifests
        ├── config_screen.py                # ⚙️  Manage airports & routes
        └── manage_reservations_screen.py   # 🔧 Cancel/reactivate reservations
```

### Database Schema

The system uses a normalized relational database with the following tables:

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| **airports** | Store airport information | code, name, city, active |
| **routes** | Define flight routes between airports | origin, destination, flight_number |
| **flights** | Scheduled flight instances | route_id, departure_time, flight_date, capacity |
| **passengers** | Passenger records | first_name, last_name, date_of_birth |
| **reservations** | Booking records | passenger_id, confirmation_number, status |
| **reservation_flights** | Link reservations to flights (many-to-many) | reservation_id, flight_id, seat_number |

**Key relationships:**
- Routes connect two airports (origin → destination)
- Flights are instances of routes on specific dates/times
- Reservations belong to passengers and can include multiple flights
- Seat assignments prevent double-booking via unique constraints

## 🐛 Troubleshooting

### Common Issues and Solutions

<details>
<summary><strong>Application won't start / ImportError</strong></summary>

```bash
# Check if Python curses is available
python3 -c "import curses; print('✓ Curses is available')"

# Verify Python version
python3 --version  # Should be 3.6 or higher
```

**Windows users:** Install Windows Subsystem for Linux (WSL) or:
```bash
pip install windows-curses
```
</details>

<details>
<summary><strong>Screen looks garbled or overlapping text</strong></summary>

- **Resize terminal:** Minimum 80×24 characters (100×30 recommended)
- **Check terminal size:**
  ```bash
  tput cols  # Should be ≥ 80
  tput lines # Should be ≥ 24
  ```
- **Set TERM variable:**
  ```bash
  export TERM=xterm-256color
  python3 main.py
  ```
</details>

<details>
<summary><strong>Colors not showing / monochrome display</strong></summary>

```bash
# Check terminal supports colors
echo $TERM  # Should be something like xterm-256color

# Test color support
python3 -c "import curses; print(curses.has_colors())"
```

Most modern terminals support colors. Try: iTerm2, GNOME Terminal, or Alacritty
</details>

<details>
<summary><strong>Database errors / corrupt data</strong></summary>

**Reset the database:**
```bash
rm kidairlines.db
python3 main.py
```

This will recreate the database with fresh sample data.
</details>

<details>
<summary><strong>ESC key not working (macOS)</strong></summary>

Some terminals may have ESC key conflicts. Try:
- Use `Ctrl+[` as alternative to ESC
- Check terminal settings for ESC key binding
</details>

## 🎓 Educational Use

KidAirlines is perfect for:
- Teaching database concepts (SQL, relationships)
- Learning terminal UI programming (curses)
- Understanding reservation system architecture
- Practicing Python programming
- Experiencing retro computing interfaces

## 📝 Notes

- This is a **simulation** - not connected to real airlines!
- Designed for **educational and entertainment** purposes
- Data is stored locally and never transmitted
- Perfect for kids learning about travel and computers

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test thoroughly** (book tickets, view manifests, etc.)
5. **Commit your changes** (`git commit -m 'Add amazing feature'`)
6. **Push to branch** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

### Development Guidelines

- Follow existing code style (see [CLAUDE.md](CLAUDE.md))
- Use snake_case for functions and variables
- Add docstrings to public methods
- Test manually using the application
- Keep the retro aesthetic consistent

### Ideas for Contributions

- 🔍 Add search functionality for passengers/flights
- 📊 Create reporting features (most popular routes, occupancy rates)
- 🎨 New color schemes or themes
- 📝 Better error messages and validation
- 🌐 Multi-language support
- ♿ Accessibility improvements
- 📱 Responsive terminal sizing

## 👨‍💻 For Developers

### Developer Documentation

Comprehensive technical documentation available:

| Document | Contents |
|----------|----------|
| **[CLAUDE.md](CLAUDE.md)** | Complete developer guide: architecture, patterns, maintenance tasks, API reference |
| **schema.sql** | Full database schema with relationships and constraints |
| **src/models/** | Model layer documentation and query examples |

### Quick Development Commands

```bash
# Reset database to fresh state
rm kidairlines.db && python3 main.py

# Initialize database only (no UI)
python3 src/database/db_init.py

# Check database contents
python3 -c "
import sys; sys.path.insert(0, 'src')
from src.models import Airport, Flight, Reservation
print(f'Airports: {len(Airport.get_all())}')
print(f'Flights: {len(Flight.get_all())}')
print(f'Reservations: {len(Reservation.get_all())}')
"
```

### Code Structure Philosophy

- **Models** handle all database operations (no SQL in UI code)
- **Screens** extend `ScreenBase` and use reusable components
- **Menu/ListSelector** components for consistent navigation
- **Static methods** for model operations (no instantiation needed)

## 🌟 Features Roadmap

Future enhancements being considered:

- [ ] Multi-leg trip booking wizard
- [ ] ASCII art boarding passes
- [ ] Seat map visualization
- [ ] Standby list for full flights
- [ ] Frequent flyer program
- [ ] Export reservations to CSV
- [ ] Flight search by route/airport
- [ ] Calendar view for date selection
- [ ] Help screen with keyboard shortcuts

## 📄 License

This project is provided as-is for educational and entertainment purposes.

## 🙏 Acknowledgments

- Inspired by classic SABRE and Apollo reservation systems
- Built with ❤️ for kids who love aviation
- Thanks to the Python community for excellent documentation

## 📧 Contact & Support

- **Issues:** Report bugs on [GitHub Issues](https://github.com/yourusername/kidairlines/issues)
- **Questions:** Open a [Discussion](https://github.com/yourusername/kidairlines/discussions)
- **Contributing:** See [Contributing](#-contributing) section above

---

<div align="center">

## ✈️ Happy Flying! ✈️

**Experience the golden age of airline reservations**

Made with 💚 for kids and retro computing enthusiasts

[⬆ Back to Top](#-kidairlines)

</div>
