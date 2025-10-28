from .database import execute_query, execute_update


class Route:
    def __init__(self, id, origin_airport_id, destination_airport_id, flight_number,
                 origin_code=None, origin_name=None, origin_city=None,
                 dest_code=None, dest_name=None, dest_city=None):
        self.id = id
        self.origin_airport_id = origin_airport_id
        self.destination_airport_id = destination_airport_id
        self.flight_number = flight_number
        self.origin_code = origin_code
        self.origin_name = origin_name
        self.origin_city = origin_city
        self.dest_code = dest_code
        self.dest_name = dest_name
        self.dest_city = dest_city

    @staticmethod
    def get_all():
        """Get all routes with airport details"""
        query = """
            SELECT r.*,
                   o.code as origin_code, o.name as origin_name, o.city as origin_city,
                   d.code as dest_code, d.name as dest_name, d.city as dest_city
            FROM routes r
            JOIN airports o ON r.origin_airport_id = o.id
            JOIN airports d ON r.destination_airport_id = d.id
            ORDER BY r.flight_number
        """
        rows = execute_query(query)
        return [Route(**dict(row)) for row in rows]

    @staticmethod
    def get_by_id(route_id):
        """Get route by ID"""
        query = """
            SELECT r.*,
                   o.code as origin_code, o.name as origin_name, o.city as origin_city,
                   d.code as dest_code, d.name as dest_name, d.city as dest_city
            FROM routes r
            JOIN airports o ON r.origin_airport_id = o.id
            JOIN airports d ON r.destination_airport_id = d.id
            WHERE r.id = ?
        """
        rows = execute_query(query, (route_id,))
        if rows:
            return Route(**dict(rows[0]))
        return None

    @staticmethod
    def create(origin_airport_id, destination_airport_id, flight_number):
        """Create a new route"""
        query = "INSERT INTO routes (origin_airport_id, destination_airport_id, flight_number) VALUES (?, ?, ?)"
        route_id = execute_update(query, (origin_airport_id, destination_airport_id, flight_number))
        return route_id

    @staticmethod
    def delete(route_id):
        """Delete a route"""
        query = "DELETE FROM routes WHERE id = ?"
        execute_update(query, (route_id,))

    def __str__(self):
        return f"{self.flight_number}: {self.origin_code} -> {self.dest_code}"
