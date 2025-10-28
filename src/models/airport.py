from .database import execute_query, execute_update


class Airport:
    def __init__(self, id, code, name, city, active):
        self.id = id
        self.code = code
        self.name = name
        self.city = city
        self.active = active

    @staticmethod
    def get_all(active_only=True):
        """Get all airports"""
        query = "SELECT * FROM airports"
        if active_only:
            query += " WHERE active = 1"
        query += " ORDER BY code"

        rows = execute_query(query)
        return [Airport(**dict(row)) for row in rows]

    @staticmethod
    def get_by_id(airport_id):
        """Get airport by ID"""
        query = "SELECT * FROM airports WHERE id = ?"
        rows = execute_query(query, (airport_id,))
        if rows:
            return Airport(**dict(rows[0]))
        return None

    @staticmethod
    def get_by_code(code):
        """Get airport by code"""
        query = "SELECT * FROM airports WHERE code = ?"
        rows = execute_query(query, (code,))
        if rows:
            return Airport(**dict(rows[0]))
        return None

    @staticmethod
    def create(code, name, city):
        """Create a new airport"""
        query = "INSERT INTO airports (code, name, city, active) VALUES (?, ?, ?, 1)"
        airport_id = execute_update(query, (code, name, city))
        return airport_id

    @staticmethod
    def update_status(airport_id, active):
        """Update airport active status"""
        query = "UPDATE airports SET active = ? WHERE id = ?"
        execute_update(query, (active, airport_id))

    def __str__(self):
        return f"{self.code} - {self.name} ({self.city})"
