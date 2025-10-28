-- KidAirlines Database Schema

CREATE TABLE IF NOT EXISTS airports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin_airport_id INTEGER NOT NULL,
    destination_airport_id INTEGER NOT NULL,
    flight_number TEXT NOT NULL,
    FOREIGN KEY (origin_airport_id) REFERENCES airports(id),
    FOREIGN KEY (destination_airport_id) REFERENCES airports(id),
    UNIQUE(flight_number)
);

CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_id INTEGER NOT NULL,
    departure_time TEXT NOT NULL,
    arrival_time TEXT NOT NULL,
    flight_date TEXT NOT NULL,
    capacity INTEGER DEFAULT 100,
    FOREIGN KEY (route_id) REFERENCES routes(id)
);

CREATE TABLE IF NOT EXISTS passengers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_id INTEGER NOT NULL,
    confirmation_number TEXT UNIQUE NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'CONFIRMED',
    FOREIGN KEY (passenger_id) REFERENCES passengers(id)
);

CREATE TABLE IF NOT EXISTS reservation_flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reservation_id INTEGER NOT NULL,
    flight_id INTEGER NOT NULL,
    seat_number TEXT,
    FOREIGN KEY (reservation_id) REFERENCES reservations(id),
    FOREIGN KEY (flight_id) REFERENCES flights(id),
    UNIQUE(flight_id, seat_number)
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_flights_date ON flights(flight_date);
CREATE INDEX IF NOT EXISTS idx_reservations_passenger ON reservations(passenger_id);
CREATE INDEX IF NOT EXISTS idx_reservation_flights_reservation ON reservation_flights(reservation_id);
CREATE INDEX IF NOT EXISTS idx_reservation_flights_flight ON reservation_flights(flight_id);
