import sqlite3
import os
from datetime import datetime, timedelta
import random
import string


def get_db_path():
    """Get the path to the database file"""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'kidairlines.db')


def init_database():
    """Initialize the database with schema"""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read and execute schema
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema = f.read()

    cursor.executescript(schema)
    conn.commit()

    # Check if we need to seed data
    cursor.execute("SELECT COUNT(*) FROM airports")
    if cursor.fetchone()[0] == 0:
        seed_data(conn)

    conn.close()
    print(f"Database initialized at: {db_path}")


def seed_data(conn):
    """Seed the database with sample data - Hub-and-Spoke network centered on EWR"""
    cursor = conn.cursor()

    # Airports - EWR as hub with domestic and international destinations
    airports = [
        ('EWR', 'Newark Liberty International Airport', 'Newark'),        # Hub - ID 1
        ('DTW', 'Detroit Metropolitan Wayne County Airport', 'Detroit'),  # ID 2
        ('ORD', 'O\'Hare International Airport', 'Chicago'),             # ID 3
        ('PBI', 'Palm Beach International Airport', 'West Palm Beach'),  # ID 4
        ('BWI', 'Baltimore/Washington International', 'Baltimore'),      # ID 5
        ('MIA', 'Miami International Airport', 'Miami'),                 # ID 6
        ('DPS', 'Ngurah Rai International Airport', 'Bali'),            # ID 7
        ('CAI', 'Cairo International Airport', 'Cairo'),                 # ID 8
        ('CDG', 'Charles de Gaulle Airport', 'Paris'),                  # ID 9
        ('LHR', 'London Heathrow Airport', 'London'),                   # ID 10
        ('SFO', 'San Francisco International Airport', 'San Francisco'), # ID 11
        ('OMA', 'Eppley Airfield', 'Omaha'),                           # ID 12
    ]

    cursor.executemany(
        "INSERT INTO airports (code, name, city, active) VALUES (?, ?, ?, 1)",
        airports
    )

    # Hub-and-Spoke routes - All routes connect to/from EWR (airport ID 1)
    routes = [
        # EWR to destinations
        (1, 2, 'KA100'),   # EWR -> DTW
        (1, 3, 'KA110'),   # EWR -> ORD
        (1, 4, 'KA120'),   # EWR -> PBI
        (1, 5, 'KA130'),   # EWR -> BWI
        (1, 6, 'KA140'),   # EWR -> MIA
        (1, 7, 'KA200'),   # EWR -> DPS (Bali)
        (1, 8, 'KA210'),   # EWR -> CAI (Cairo)
        (1, 9, 'KA220'),   # EWR -> CDG (Paris)
        (1, 10, 'KA230'),  # EWR -> LHR (London)
        (1, 11, 'KA240'),  # EWR -> SFO
        (1, 12, 'KA250'),  # EWR -> OMA

        # Return routes to EWR
        (2, 1, 'KA101'),   # DTW -> EWR
        (3, 1, 'KA111'),   # ORD -> EWR
        (4, 1, 'KA121'),   # PBI -> EWR
        (5, 1, 'KA131'),   # BWI -> EWR
        (6, 1, 'KA141'),   # MIA -> EWR
        (7, 1, 'KA201'),   # DPS -> EWR
        (8, 1, 'KA211'),   # CAI -> EWR
        (9, 1, 'KA221'),   # CDG -> EWR
        (10, 1, 'KA231'),  # LHR -> EWR
        (11, 1, 'KA241'),  # SFO -> EWR
        (12, 1, 'KA251'),  # OMA -> EWR
    ]

    cursor.executemany(
        "INSERT INTO routes (origin_airport_id, destination_airport_id, flight_number) VALUES (?, ?, ?)",
        routes
    )

    # Realistic flight durations and schedules (in hours:minutes)
    # Format: route_id: [(departure_time, duration_in_minutes, capacity), ...]
    route_schedules = {
        # Outbound from EWR
        1: [('06:00', 120, 150), ('12:00', 120, 150), ('18:00', 120, 150)],  # EWR->DTW (2h)
        2: [('07:00', 150, 180), ('13:30', 150, 180), ('19:00', 150, 180)],  # EWR->ORD (2.5h)
        3: [('08:00', 180, 150), ('14:00', 180, 150), ('20:00', 180, 150)],  # EWR->PBI (3h)
        4: [('06:30', 60, 120), ('10:00', 60, 120), ('14:00', 60, 120), ('18:00', 60, 120)],  # EWR->BWI (1h)
        5: [('07:30', 180, 180), ('12:00', 180, 180), ('17:00', 180, 180)],  # EWR->MIA (3h)
        6: [('20:00', 1140, 250)],  # EWR->DPS Bali (19h) - overnight long-haul
        7: [('19:30', 660, 250)],   # EWR->CAI Cairo (11h) - overnight
        8: [('18:00', 450, 220), ('21:30', 450, 220)],  # EWR->CDG Paris (7.5h)
        9: [('19:00', 420, 220), ('22:00', 420, 220)],  # EWR->LHR London (7h)
        10: [('08:00', 370, 180), ('14:00', 370, 180), ('20:00', 370, 180)],  # EWR->SFO (6h 10m)
        11: [('09:00', 180, 150), ('15:00', 180, 150)],  # EWR->OMA Omaha (3h)

        # Inbound to EWR
        12: [('08:00', 120, 150), ('14:00', 120, 150), ('20:00', 120, 150)],  # DTW->EWR (2h)
        13: [('06:00', 150, 180), ('11:30', 150, 180), ('17:00', 150, 180)],  # ORD->EWR (2.5h)
        14: [('07:00', 180, 150), ('13:00', 180, 150), ('19:00', 180, 150)],  # PBI->EWR (3h)
        15: [('07:00', 60, 120), ('11:00', 60, 120), ('15:00', 60, 120), ('19:00', 60, 120)],  # BWI->EWR (1h)
        16: [('06:30', 180, 180), ('11:00', 180, 180), ('16:00', 180, 180)],  # MIA->EWR (3h)
        17: [('22:00', 1080, 250)],  # DPS->EWR (18h) - overnight long-haul
        18: [('23:00', 660, 250)],   # CAI->EWR (11h) - overnight
        19: [('10:00', 480, 220), ('13:30', 480, 220)],  # CDG->EWR (8h) - westbound adds time
        20: [('09:00', 450, 220), ('12:00', 450, 220)],  # LHR->EWR (7.5h) - westbound
        21: [('07:00', 340, 180), ('13:00', 340, 180), ('19:00', 340, 180)],  # SFO->EWR (5h 40m) - tailwind
        22: [('08:00', 180, 150), ('14:00', 180, 150)],  # OMA->EWR (3h)
    }

    def calculate_arrival_time(departure, duration_minutes):
        """Calculate arrival time given departure and duration"""
        dep_hour, dep_min = map(int, departure.split(':'))
        total_minutes = dep_hour * 60 + dep_min + duration_minutes

        # Handle next-day arrivals
        arr_hour = (total_minutes // 60) % 24
        arr_min = total_minutes % 60

        return f"{arr_hour:02d}:{arr_min:02d}"

    # Generate flights for the next 7 days
    today = datetime.now()
    for day_offset in range(7):
        flight_date = (today + timedelta(days=day_offset)).strftime('%Y-%m-%d')

        for route_id, schedules in route_schedules.items():
            for departure, duration, capacity in schedules:
                arrival = calculate_arrival_time(departure, duration)

                cursor.execute(
                    "INSERT INTO flights (route_id, departure_time, arrival_time, flight_date, capacity) VALUES (?, ?, ?, ?, ?)",
                    (route_id, departure, arrival, flight_date, capacity)
                )

    # Sample passengers
    first_names = ['Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']

    for first in first_names[:5]:
        for last in last_names[:3]:
            cursor.execute(
                "INSERT INTO passengers (first_name, last_name, date_of_birth) VALUES (?, ?, ?)",
                (first, last, '2010-05-15')
            )

    # Sample reservations
    for i in range(5):
        conf_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        passenger_id = random.randint(1, 15)

        cursor.execute(
            "INSERT INTO reservations (passenger_id, confirmation_number, status) VALUES (?, ?, 'CONFIRMED')",
            (passenger_id, conf_number)
        )

        reservation_id = cursor.lastrowid
        flight_id = random.randint(1, 50)
        seat = f"{random.randint(1, 25)}{random.choice('ABCDEF')}"

        try:
            cursor.execute(
                "INSERT INTO reservation_flights (reservation_id, flight_id, seat_number) VALUES (?, ?, ?)",
                (reservation_id, flight_id, seat)
            )
        except sqlite3.IntegrityError:
            pass  # Skip if seat already taken

    conn.commit()
    print("Sample data seeded successfully")


if __name__ == '__main__':
    init_database()
