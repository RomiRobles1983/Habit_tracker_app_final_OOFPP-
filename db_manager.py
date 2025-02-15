import sqlite3
from datetime import datetime

class HabitDatabase:
    def __init__(self, db_name="habits.db"):
        """Initialize the database connection and create necessary tables."""
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """Create the habits and completion_dates tables if they don't exist."""
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                creation_date TEXT NOT NULL
            )
            """)
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS completion_dates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completion_datetime TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(id)
            )
            """)

    def insert_habit(self, name, periodicity):
        """Insert a new habit into the habits table."""
        with self.conn:
            self.conn.execute("""
            INSERT INTO habits (name, periodicity, creation_date)
            VALUES (?, ?, ?)
            """, (name, periodicity, datetime.now().strftime("%Y-%m-%d")))

    def delete_habit(self, habit_id):
        """Delete a habit by its ID."""
        with self.conn:
            # Eliminate the completion dates associated with this habit first.
            self.conn.execute("""
            DELETE FROM completion_dates WHERE habit_id = ?
            """, (habit_id,))
            
            # Now eliminate the habit itself
            self.conn.execute("""
            DELETE FROM habits WHERE id = ?
            """, (habit_id,))
           
    def get_habit_by_id(self, habit_id):
        """Retrieve a single habit by its ID."""
        with self.conn:
            return self.conn.execute("SELECT * FROM habits WHERE id = ?", (habit_id,)).fetchone()
    

    def mark_habit_completed(self, habit_id,completion_datetime):
        """Mark a habit as completed by inserting a completion date and time into the database."""
        # Check if the habit exists
        habits = self.get_habits()
        if not any(h[0] == habit_id for h in habits):
            raise ValueError(f"No habit found with ID {habit_id}.")
        
        # Insert the date and time of completion
        self.insert_completion_datetime(habit_id, completion_datetime)
        print(f"Habit with ID {habit_id} has been marked as completed at {completion_datetime}.")


    def insert_completion_datetime(self, habit_id, completion_datetime):
        """Insert a completion date and time for a specific habit."""
        with self.conn:
            self.conn.execute("""
            INSERT INTO completion_dates (habit_id, completion_datetime)
            VALUES (?, ?)
            """, (habit_id, completion_datetime))


    def get_habits(self):
        """Retrieve all habits from the habits table."""
        with self.conn:
            return self.conn.execute("SELECT * FROM habits").fetchall()
        

    def get_habits_by_periodicity(self, periodicity):
        """Retrieve all habits with a specific periodicity (daily or weekly)."""
        with self.conn:
            return self.conn.execute("""
            SELECT * FROM habits WHERE periodicity = ?
            """, (periodicity,)).fetchall()
        

    def get_completion_dates(self, habit_id):
        """Retrieve all completion dates for a specific habit."""
        with self.conn:
            return self.conn.execute("""
            SELECT completion_datetime FROM completion_dates
            WHERE habit_id = ?
            """, (habit_id,)).fetchall()
        
        
    def delete_all_habits(self):
        """Elimina todos los hábitos y sus registros de completado en la base de datos."""
        with self.conn:
             self.conn.execute("DELETE FROM completion_dates")  # Remove all dates from completed
             self.conn.execute("DELETE FROM habits")  # Eliminate all habits


    def close(self):
        """Close the database connection."""
        self.conn.close()


