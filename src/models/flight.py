from .database import execute_query, execute_update


class Flight:
    def __init__(self, id, route_id, departure_time, arrival_time, flight_date, capacity,
                 flight_number=None, origin_code=None, dest_code=None,
                 origin_city=None, dest_city=None):
        self.id = id
        self.route_id = route_id
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.flight_date = flight_date
        self.capacity = capacity
        self.flight_number = flight_number
        self.origin_code = origin_code
        self.dest_code = dest_code
        self.origin_city = origin_city
        self.dest_city = dest_city

    @staticmethod
    def get_all(date_filter=None):
        """Get all flights with route and airport details"""
        query = """
            SELECT f.*, r.flight_number,
                   o.code as origin_code, o.city as origin_city,
                   d.code as dest_code, d.city as dest_city
            FROM flights f
            JOIN routes r ON f.route_id = r.id
            JOIN airports o ON r.origin_airport_id = o.id
            JOIN airports d ON r.destination_airport_id = d.id
        """
        params = None
        if date_filter:
            query += " WHERE f.flight_date = ?"
            params = (date_filter,)

        query += " ORDER BY f.flight_date, f.departure_time"

        rows = execute_query(query, params)
        return [Flight(**dict(row)) for row in rows]

    @staticmethod
    def get_by_id(flight_id):
        """Get flight by ID"""
        query = """
            SELECT f.*, r.flight_number,
                   o.code as origin_code, o.city as origin_city,
                   d.code as dest_code, d.city as dest_city
            FROM flights f
            JOIN routes r ON f.route_id = r.id
            JOIN airports o ON r.origin_airport_id = o.id
            JOIN airports d ON r.destination_airport_id = d.id
            WHERE f.id = ?
        """
        rows = execute_query(query, (flight_id,))
        if rows:
            return Flight(**dict(rows[0]))
        return None

    @staticmethod
    def get_available_seats(flight_id):
        """Get number of available seats on a flight"""
        query = """
            SELECT f.capacity - COUNT(rf.id) as available
            FROM flights f
            LEFT JOIN reservation_flights rf ON f.id = rf.flight_id
            WHERE f.id = ?
            GROUP BY f.id, f.capacity
        """
        rows = execute_query(query, (flight_id,))
        if rows:
            return rows[0]['available']
        return 0

    @staticmethod
    def create(route_id, departure_time, arrival_time, flight_date, capacity=150):
        """Create a new flight"""
        query = "INSERT INTO flights (route_id, departure_time, arrival_time, flight_date, capacity) VALUES (?, ?, ?, ?, ?)"
        flight_id = execute_update(query, (route_id, departure_time, arrival_time, flight_date, capacity))
        return flight_id

    def __str__(self):
        return f"{self.flight_number} on {self.flight_date} {self.departure_time}: {self.origin_code} -> {self.dest_code}"
