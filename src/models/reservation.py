from .database import execute_query, execute_update
import random
import string


class Reservation:
    def __init__(self, id, passenger_id, confirmation_number, created_at=None, status='CONFIRMED',
                 passenger_first_name=None, passenger_last_name=None):
        self.id = id
        self.passenger_id = passenger_id
        self.confirmation_number = confirmation_number
        self.created_at = created_at
        self.status = status
        self.passenger_first_name = passenger_first_name
        self.passenger_last_name = passenger_last_name

    @staticmethod
    def generate_confirmation_number():
        """Generate a random 6-character confirmation number"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    @staticmethod
    def get_all():
        """Get all reservations with passenger details"""
        query = """
            SELECT r.*, p.first_name as passenger_first_name, p.last_name as passenger_last_name
            FROM reservations r
            JOIN passengers p ON r.passenger_id = p.id
            ORDER BY r.created_at DESC
        """
        rows = execute_query(query)
        return [Reservation(**dict(row)) for row in rows]

    @staticmethod
    def get_by_id(reservation_id):
        """Get reservation by ID"""
        query = """
            SELECT r.*, p.first_name as passenger_first_name, p.last_name as passenger_last_name
            FROM reservations r
            JOIN passengers p ON r.passenger_id = p.id
            WHERE r.id = ?
        """
        rows = execute_query(query, (reservation_id,))
        if rows:
            return Reservation(**dict(rows[0]))
        return None

    @staticmethod
    def get_by_confirmation(confirmation_number):
        """Get reservation by confirmation number"""
        query = """
            SELECT r.*, p.first_name as passenger_first_name, p.last_name as passenger_last_name
            FROM reservations r
            JOIN passengers p ON r.passenger_id = p.id
            WHERE r.confirmation_number = ?
        """
        rows = execute_query(query, (confirmation_number,))
        if rows:
            return Reservation(**dict(rows[0]))
        return None

    @staticmethod
    def get_by_passenger(passenger_id):
        """Get all reservations for a passenger"""
        query = """
            SELECT r.*, p.first_name as passenger_first_name, p.last_name as passenger_last_name
            FROM reservations r
            JOIN passengers p ON r.passenger_id = p.id
            WHERE r.passenger_id = ?
            ORDER BY r.created_at DESC
        """
        rows = execute_query(query, (passenger_id,))
        return [Reservation(**dict(row)) for row in rows]

    @staticmethod
    def create(passenger_id, confirmation_number=None):
        """Create a new reservation"""
        if not confirmation_number:
            confirmation_number = Reservation.generate_confirmation_number()

        query = "INSERT INTO reservations (passenger_id, confirmation_number, status) VALUES (?, ?, 'CONFIRMED')"
        reservation_id = execute_update(query, (passenger_id, confirmation_number))
        return reservation_id, confirmation_number

    @staticmethod
    def update_status(reservation_id, status):
        """Update reservation status"""
        query = "UPDATE reservations SET status = ? WHERE id = ?"
        execute_update(query, (status, reservation_id))

    @staticmethod
    def delete(reservation_id):
        """Delete a reservation and its flights"""
        # Delete reservation flights first
        execute_update("DELETE FROM reservation_flights WHERE reservation_id = ?", (reservation_id,))
        # Delete reservation
        execute_update("DELETE FROM reservations WHERE id = ?", (reservation_id,))

    def get_flights(self):
        """Get all flights for this reservation"""
        query = """
            SELECT rf.*, f.flight_date, f.departure_time, f.arrival_time,
                   r.flight_number, o.code as origin_code, d.code as dest_code,
                   o.city as origin_city, d.city as dest_city
            FROM reservation_flights rf
            JOIN flights f ON rf.flight_id = f.id
            JOIN routes r ON f.route_id = r.id
            JOIN airports o ON r.origin_airport_id = o.id
            JOIN airports d ON r.destination_airport_id = d.id
            WHERE rf.reservation_id = ?
            ORDER BY f.flight_date, f.departure_time
        """
        rows = execute_query(query, (self.id,))
        return [dict(row) for row in rows]

    @staticmethod
    def add_flight(reservation_id, flight_id, seat_number=None):
        """Add a flight to a reservation"""
        query = "INSERT INTO reservation_flights (reservation_id, flight_id, seat_number) VALUES (?, ?, ?)"
        try:
            execute_update(query, (reservation_id, flight_id, seat_number))
            return True
        except Exception as e:
            return False

    @staticmethod
    def remove_flight(reservation_id, flight_id):
        """Remove a flight from a reservation"""
        query = "DELETE FROM reservation_flights WHERE reservation_id = ? AND flight_id = ?"
        execute_update(query, (reservation_id, flight_id))

    def passenger_name(self):
        if self.passenger_first_name and self.passenger_last_name:
            return f"{self.passenger_first_name} {self.passenger_last_name}"
        return "Unknown"

    def __str__(self):
        return f"Reservation {self.confirmation_number} - {self.passenger_name()} ({self.status})"
