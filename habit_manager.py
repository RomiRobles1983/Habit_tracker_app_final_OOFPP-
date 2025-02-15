from db_manager import HabitDatabase
from datetime import datetime

class HabitManager:
    def __init__(self):
        """Initialize the habit manager and database connection."""
        self.db = HabitDatabase()


    def create_habit(self, name, periodicity):
        """Create a new habit with the given name and periodicity."""
        if not name or not periodicity:
            raise ValueError("Name and periodicity are required to create a habit.")
        existing_habits = self.db.get_habits()
        if any(h[1].lower() == name.lower() for h in existing_habits):
            raise ValueError(f"The habit '{name}' already exists.")
        
        # Inserting the habit into the database
        self.db.insert_habit(name, periodicity)
        print(f"Habit '{name}' with periodicity '{periodicity}' has been created.")


    def delete_habit(self, habit_id):
        """Delete a habit by its ID with validation checks."""
        habits = self.db.get_habits()
        if not habits:
            raise ValueError("No habits found in the database.")

        habit = self.db.get_habit_by_id(habit_id)
        if not habit:
            raise ValueError(f"No habit found with ID {habit_id}.")

        self.db.delete_habit(habit_id)
        print(f"Habit with ID {habit_id} has been deleted.")

        
    def mark_habit_completed(self, habit_id, completion_datetime):
        """Mark a habit as completed."""
        habits = self.db.get_habits()
        if not any(h[0] == habit_id for h in habits):
            raise ValueError(f"No habit found with ID {habit_id}.")
        
        now = datetime.now()
        if completion_datetime > now:
            raise ValueError("Completion date cannot be in the future.")
        
        self.db.insert_completion_datetime(habit_id, completion_datetime)
        print(f"Habit with ID {habit_id} has been marked as completed at {completion_datetime}.")
        

    def close(self):
        """Close the database connection."""
        self.db.close()



