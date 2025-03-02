import click
from db_manager import HabitDatabase
from analytics import Analytics
from habit_manager import HabitManager  
from datetime import datetime
import json

# Single instance for interacting with the database and analysis
db = HabitDatabase("habits.db")
analytics = Analytics(db)

@click.group()
def cli():
    """Habit Tracker CLI"""
    click.echo("Welcome to Habit Tracker CLI!")
    click.echo("Usage: main.py [OPTIONS] COMMAND [ARGS]...")


@cli.command()
def load_predefined_habits():
    """Delete existing habits and load predefined habits from a JSON file."""
    try:
        # Opens the JSON file with the default habits
        with open('habit_data.json', 'r') as f:
            habit_data = json.load(f)
        
        habit_manager = HabitManager()
        
        # Eliminate all existing habits before loading new habits
        with db.conn:
            db.delete_all_habits()
        click.echo("Previous habits deleted.")

        # Inserting the new habits
        for habit in habit_data['habits']:
            habit_manager.create_habit(habit['name'], habit['periodicity'])
            
            
            habits = db.get_habits()  
            habit_id = next((h[0] for h in habits if h[1] == habit['name']), None)

            if habit_id:
                for completion_datetime_str in habit['completion_datetime']:
                    completion_datetime = datetime.strptime(completion_datetime_str, "%Y-%m-%d %H:%M:%S")
                    habit_manager.mark_habit_completed(habit_id, completion_datetime)
        
        click.echo("Predefined habits loaded successfully!")

    except FileNotFoundError:
        click.echo("Error: 'habit_data.json' file not found.")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

# Command to create a habit
@cli.command()
@click.argument('name')
@click.argument('periodicity', type=click.Choice(['daily', 'weekly'], case_sensitive=False))
def create(name, periodicity):
    """Create a new habit with a name and periodicity (daily/weekly)."""
    try:
        habit_manager = HabitManager()  # Instantiate HabitManager
        habit_manager.create_habit(name, periodicity)  # Call create_habit method from HabitManager
        click.echo(f"Created habit: {name} with periodicity: {periodicity}")
    except ValueError as e:
        click.echo(f"Error: {str(e)}")  # Handle any error, such as a duplicate habit name

# Command to eliminate a habit
@cli.command()
@click.argument('habit_id', type=int)
def delete(habit_id):
    """Delete a habit by its ID."""
    try:
        habit_manager = HabitManager()  # Instantiate HabitManager
        habit_manager.delete_habit(habit_id)  # Call delete_habit method from HabitManager
        click.echo(f"Deleted habit with ID: {habit_id}")
    except ValueError as e:
        click.echo(f"Error: {str(e)}") 

# Command to mark a habit as completed
@cli.command()
@click.argument('habit_id', type=int)
@click.argument('datetime_str')
def complete(habit_id, datetime_str):
    """Mark a habit as completed with a manually entered date and time (YYYY-MM-DD HH:MM:SS)."""
    try:
        # Converts the date that comes as a string to a datetime object
        completion_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        click.echo("Error: Incorrect datetime format. Use 'YYYY-MM-DD HH:MM:SS'.")
        return

    try:
        habit_manager = HabitManager()
        habit_manager.mark_habit_completed(habit_id, completion_datetime)  # We pass datetime directly
        
    except ValueError as e:
        click.echo(f"Error: {str(e)}")

# Command to list all current habits
@cli.command()
def list_habits():
    """List all current habits."""
    click.echo("Current habits:")
    habits = db.get_habits()
    for habit in habits:
        click.echo(f"ID: {habit[0]}, Name: {habit[1]}, Periodicity: {habit[2]}")

# Command to list habits by periodicity
@cli.command()
@click.argument('periodicity', type=click.Choice(['daily', 'weekly'], case_sensitive=False))
def list_by_periodicity(periodicity):
    """List all habits with a specific periodicity (daily or weekly)."""
    habits = db.get_habits_by_periodicity(periodicity)
    if habits:
        click.echo(f"Habits with periodicity '{periodicity}':")
        for habit in habits:
            click.echo(f"ID: {habit[0]}, Name: {habit[1]}, Created At: {habit[3]}")
    else:
        click.echo(f"No habits found with periodicity '{periodicity}'.")


# Command to query streaks
@cli.command()
@click.argument('habit_id', type=int)
def longest_streak_per_habit(habit_id):
    """Show the longest streak for a specific habit."""
    
    # Get the habit and its periodicity
    habit = db.get_habit_by_id(habit_id)
    
    if habit:
        habit_periodicity = habit[2]  # Assuming periodicity is in index 2 of the tuple
        longest_streak = analytics.get_longest_streak_for_habit(habit_id)
        
        # Display the longest streak
        click.echo(f"The longest streak for habit with ID {habit_id} is {longest_streak} {'weeks' if habit_periodicity == 'weekly' else 'days'}.")
    else:
        click.echo(f"No habit found with ID {habit_id}.")


# Command to look up the longest overall streak
@cli.command()
def longest_streak():
    """Show the longest streak across all habits."""
    longest_streak = analytics.get_longest_streak()
    click.echo(f"The longest streak across all habits is {longest_streak} days.")

if __name__ == '__main__':
    cli()

# Close database connections when the script ends
import atexit
@atexit.register
def cleanup():
    db.close()
    analytics.close()

