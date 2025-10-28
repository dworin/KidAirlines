from .database import execute_query, execute_update


class Passenger:
    def __init__(self, id, first_name, last_name, date_of_birth=None, created_at=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.created_at = created_at

    @staticmethod
    def get_all():
        """Get all passengers"""
        query = "SELECT * FROM passengers ORDER BY last_name, first_name"
        rows = execute_query(query)
        return [Passenger(**dict(row)) for row in rows]

    @staticmethod
    def get_by_id(passenger_id):
        """Get passenger by ID"""
        query = "SELECT * FROM passengers WHERE id = ?"
        rows = execute_query(query, (passenger_id,))
        if rows:
            return Passenger(**dict(rows[0]))
        return None

    @staticmethod
    def search(search_term):
        """Search passengers by name"""
        query = """
            SELECT * FROM passengers
            WHERE first_name LIKE ? OR last_name LIKE ?
            ORDER BY last_name, first_name
        """
        search_pattern = f"%{search_term}%"
        rows = execute_query(query, (search_pattern, search_pattern))
        return [Passenger(**dict(row)) for row in rows]

    @staticmethod
    def create(first_name, last_name, date_of_birth=None):
        """Create a new passenger"""
        query = "INSERT INTO passengers (first_name, last_name, date_of_birth) VALUES (?, ?, ?)"
        passenger_id = execute_update(query, (first_name, last_name, date_of_birth))
        return passenger_id

    @staticmethod
    def update(passenger_id, first_name, last_name, date_of_birth=None):
        """Update passenger information"""
        query = "UPDATE passengers SET first_name = ?, last_name = ?, date_of_birth = ? WHERE id = ?"
        execute_update(query, (first_name, last_name, date_of_birth, passenger_id))

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()
