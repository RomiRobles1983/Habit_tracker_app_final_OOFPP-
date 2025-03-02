import pytest
from db_manager import HabitDatabase
from habit_manager import HabitManager
from datetime import datetime
from analytics import Analytics

@pytest.fixture(scope="function")

def clean_db():
    """
    Pytest fixture to provide a clean database for each test function.

    - Initializes a HabitDatabase instance connected to "habits.db".
    - Deletes all existing habits before the test to ensure a clean state.
    - Yields the database instance for use in the test.
    - Cleans up by deleting all habits again and closing the database after the test.

    This ensures that each test starts with a fresh database environment, preventing
    interference between test cases.
    """
    db = HabitDatabase("habits.db")
    db.delete_all_habits() 
    yield db 
    db.delete_all_habits()
    db.close() 

# TESTS FOR HABIT MANAGER
#1 Create a habit with valid name and periodicity
def test_create_habit_with_valid_name_and_periodicity(clean_db):
    """
    Test case to verify that a habit can be created with a valid name and periodicity.

    - Uses the clean_db fixture to ensure a fresh database state.
    - Creates a new habit with a specified name and periodicity.
    - Retrieves all habits from the database.
    - Asserts that the created habit exists in the database with the correct name and periodicity.

    This ensures that the habit creation functionality works correctly for valid inputs.
    """
    habit_name = "Exercise"
    periodicity = "daily"
    habit_manager = HabitManager()

    habit_manager.create_habit(habit_name, periodicity)

    
    habits = clean_db.get_habits()
    habit = next((h for h in habits if h[1] == habit_name), None)
    assert habit is not None # Ensure the habit was created
    assert habit[1] == habit_name # Verify the habit name
    assert habit[2] == periodicity # Verify the periodicity

#2 Create habit with empty name and correct periodicity
def test_create_habit_with_empty_name(clean_db):
    """
    Test case to verify that creating a habit with an empty name raises a ValueError.

    - Uses the clean_db fixture to ensure a fresh database state.
    - Attempts to create a habit with an empty name and a valid periodicity.
    - Expects a ValueError with the message: "Name and periodicity are required to create a habit."

    This ensures that the system enforces name validation correctly.
    """
    habit_name = ""
    periodicity = "daily"
    habit_manager = HabitManager()

    with pytest.raises(ValueError, match="Name and periodicity are required to create a habit."):
        habit_manager.create_habit(habit_name, periodicity)

#3 Create habit with the correct name and empty periodicity     
def test_create_habit_with_empty_periodicity (clean_db):
    """
    Test case to verify that creating a habit with an empty periodicity raises a ValueError.

    - Uses the clean_db fixture to ensure a fresh database state.
    - Attempts to create a habit with a valid name but an empty periodicity.
    - Expects a ValueError with the message: "Name and periodicity are required to create a habit."

    This ensures that the system enforces periodicity validation correctly.
    """
    habit_name = "Drink 2 liter water"
    periodicity = ""
    habit_manager = HabitManager()

    with pytest.raises(ValueError, match="Name and periodicity are required to create a habit."):
        habit_manager.create_habit(habit_name, periodicity)

#4 Create habit with empty name and empty periodicity
def test_create_habit_with_empty_name_andempty_periodicity(clean_db):
    """
    Test case to verify that creating a habit with both an empty name and an empty periodicity raises a ValueError.

    - Uses the clean_db fixture to ensure a fresh database state.
    - Attempts to create a habit with an empty name and an empty periodicity.
    - Expects a ValueError with the message: "Name and periodicity are required to create a habit."

    This ensures that the system enforces validation for both required fields.
    """
    habit_name = ""
    periodicity = ""
    habit_manager = HabitManager()

    with pytest.raises(ValueError, match="Name and periodicity are required to create a habit."):
        habit_manager.create_habit(habit_name, periodicity)

#5 Create a habit with a name that already exists in de Database
def test_create_habit_with_duplicate_name(clean_db):
    """
    Ensure that attempting to create a habit with a name that already exists raises a ValueError.
    """
    habit_name = "Yoga"
    periodicity = "weekly"
    habit_manager = HabitManager()

    habit_manager.create_habit(habit_name, periodicity)  # Create the first habit

    # Attempt to create a duplicate habit
    with pytest.raises(ValueError, match=f"The habit '{habit_name}' already exists."):
        habit_manager.create_habit(habit_name, periodicity)

#6 Remove habit with correct id
def test_delete_habit_with_valid_id(clean_db):
    """
    Ensure that deleting a habit by a valid ID removes it from the database.
    """
    habit_name = "Running"
    periodicity = "daily"
    
    clean_db.insert_habit(habit_name, periodicity)
    
    habits = clean_db.get_habits()
    habit_id = habits[-1][0]  # Assuming the ID is in the first column

    clean_db.delete_habit(habit_id)

    deleted_habit = clean_db.get_habit_by_id(habit_id)
    assert deleted_habit is None  # The habit should not be found in the database

#7 Remove habit with invalid id
def test_delete_habit_with_invalid_id(clean_db):
    """Test attempting to delete a habit that does not exist."""
    habit_id = 9999  # ID que no existe en la base de datos
    habit_manager = HabitManager()

    # Ensure the database has at least one habit to avoid triggering the 
    # "No habits found in the database." condition
    habits = clean_db.get_habits()
    if not habits:
        clean_db.insert_habit("Sample Habit", "daily")

    # Attempt to delete a habit with a non-existent ID
    with pytest.raises(ValueError, match=f"No habit found with ID {habit_id}."):
        habit_manager.delete_habit(habit_id)

#8 Remove habit when there when there are no habits in the database
def test_delete_habit_when_no_habits_exist(clean_db):
    """
    Test that deleting a habit when no habits exist in the database raises a ValueError.

    """
    habit_manager = HabitManager()

    # Attempt to delete a habit when there are no habits stored
    with pytest.raises(ValueError, match="No habits found in the database."):
        habit_manager.delete_habit(1)  # Trying to delete an arbitrary ID

#9 Mark a habit as completed without passing an id.
def test_mark_habit_completed_without_id(clean_db):
    """
    Test para marcar un hábito como completado sin proporcionar un ID válido.
    Esto verifica que se lance un ValueError cuando no se proporciona un ID de hábito.
    """
    habit_manager = HabitManager()

    # Intentamos marcar el hábito como completado sin pasar un ID
    completion_time = datetime(2025, 2, 12, 7, 30, 0)  # Hora de finalización

    # Comprobamos que se lance un ValueError con el mensaje correcto
    with pytest.raises(ValueError, match="No habit found with ID None."):
        habit_manager.mark_habit_completed(None, completion_time)

#10 Mark a habit with an invalid id as complete
def test_mark_habit_completed_with_invalid_id(clean_db):
    """
    Test to mark a habit as completed with an invalid ID.
    This checks that a ValueError is raised when the habit ID does not exist in the database.
    """
    habit_manager = HabitManager()

    # Using an invalid ID that does not exist in the database
    invalid_id = 9999  # Assuming 9999 is not a valid ID

    # Completion time
    completion_time = datetime(2025, 2, 12, 7, 30, 0)

    # Assert that a ValueError is raised with the appropriate message
    with pytest.raises(ValueError, match=f"No habit found with ID {invalid_id}."):
        habit_manager.mark_habit_completed(invalid_id, completion_time)
######################################################################################

#TEST DATABASE OPERATIONS

#11 Get the list of the habits when there are no habits
def test_get_habits_when_there_are_no_habits(clean_db):
    """Verifies that an empty list is returned when there are no habits in the database."""
    habit_manager = HabitManager()
    
    # Retrieve the habits, it should be empty
    habits = clean_db.get_habits()
    
    # Verify that the list of habits is empty
    assert len(habits) == 0

#12 Get the list of habits when there are habits
def test_get_habits_when_there_are_habits(clean_db):
    """Verifies that the habits are returned when there are habits in the database."""
    habit_manager = HabitManager()
    
     # Create some habits
    habit_manager.create_habit("Exercise", "daily")
    habit_manager.create_habit("Yoga", "weekly")
    habit_manager.create_habit("Drink water", "daily")
    
    # Retrieve the habits
    habits = clean_db.get_habits()
    
    # Verify that the number of habits is correct
    assert len(habits) == 3
    # Verify that the habit names are correct
    habit_names = [habit[1] for habit in habits]
    assert "Exercise" in habit_names
    assert "Yoga" in habit_names
    assert "Drink water" in habit_names

#13 Get the list of habits of a given periodicity
def test_get_habits_by_periodicity(clean_db):
    """Verify that habits are returned with a specific periodicity."""
    habit_manager = HabitManager()
    
    # Create some habits with different periodicities
    habit_manager.create_habit("Exercise", "daily")
    habit_manager.create_habit("Yoga", "weekly")
    habit_manager.create_habit("Drink water", "daily")
    
    # Retrieve the habits with "daily" periodicity
    daily_habits = clean_db.get_habits_by_periodicity("daily")
    
    # Verify that only daily habits are present
    assert len(daily_habits) == 2
    assert "Exercise" in [habit[1] for habit in daily_habits]
    assert "Drink water" in [habit[1] for habit in daily_habits]
    
    # Retrieve the habits with "weekly" periodicity
    weekly_habits = clean_db.get_habits_by_periodicity("weekly")
    
    # Verify that only the weekly habit is present
    assert len(weekly_habits) == 1
    assert "Yoga" in [habit[1] for habit in weekly_habits]


##################################################################################
#TEST FOR HABITS ANALYTICS
#14 Calculation of the longest streak when no habits are registered
def test_get_longest_streak_empty_db(clean_db):
    """Verify the calculation of the longest streak when no habits are registered."""
    analytics = Analytics(db=clean_db)
    
    # There are no habits in the database, so the longest streak should be 0
    longest_streak = analytics.get_longest_streak()
    
    assert longest_streak == 0  # There should be no streak if no habits exist

#15 Calculation of the longest streak when no habits are registered
# Calculation of daily streak with habits completed in different hours
# Calculation of daily streak with disorganized completion dates
# Calculation of the daily streak with duplicate completion dates

def test_calculate_streak_with_gaps():
    """Test with 5 dates containing gaps; the longest streak should be 3"""
    
    analytics = Analytics()

    # Example dates with gaps 
    dates = [
        ("2025-01-31 07:00:00",),
        ("2025-01-31 09:00:00",), #2 times completed at 2025-01-31
        ("2025-02-01 10:00:00",),
        ("2025-02-02 09:00:00",),
        ("2025-02-05 08:00:00",),  # unorganised dates
        ("2025-02-04 09:00:00",),  # Gap of 2 days
        ("2025-02-07 11:00:00",)   # Gap of 2 days
    ]

    # Convert dates to the expected format and calculate the streak
    streak = analytics._calculate_streak(dates, "daily")

    # The longest streak should be 2
    assert streak == 3, f"Expected streak to be 3, but got {streak}"

#16 Calculation of the weekly habit streak are gaps
# Calculation of weekly streak disorganized completion dates
# Calculation of weekly streak of habits with duplicate completion dates (2 times in the same week)

def test_calculate_streak_weekly():
    """Test the weekly streak calculation with consecutive dates in different weeks."""
    
    analytics = Analytics()

    # Completion dates in consecutive weeks
    dates = [
        ("2024-01-08 10:00:00",), #1 wen
        ("2024-01-09 10:00:00",), #2 time the same week
        ("2024-01-16 09:00:00",),  #2 th
        ("2024-02-05 08:00:00",),  # disorganized
        ("2024-01-25 09:00:00",),  # 3
        ("2024-02-06 11:00:00",),  
    ]

    streak = analytics._calculate_streak(dates, "weekly")

    assert streak == 3, f"Expected streak to be 3, but got {streak}"


#17 Calculate the longest streak for a particular habit, passing as an argument the id of the habit.
def test_get_longest_streak_for_habit(clean_db):
    """Verify that the function correctly returns the longest streak for a habit."""
    analytics = Analytics(db=clean_db)
    habit_manager = HabitManager()

    # Creating a new habit
    habit_manager.create_habit("Meditation", "daily")
    habit_id = clean_db.get_habits()[0][0]  # Get the ID of the habit created

    # Dates simulating a broken streak
    dates = [
        ("2025-02-01 08:00:00",),  # 1
        ("2025-02-02 09:00:00",),  # 2
        ("2025-02-03 10:00:00",),  # 3
        # Break: 2025-02-04 and 2025-02-05 missing
        ("2025-02-06 08:00:00",),  # 1
        ("2025-02-07 09:00:00",),  # 2
        ("2025-02-08 10:00:00",),  # 3
        ("2025-02-09 08:00:00",),  # 4
        ("2025-02-10 08:00:00",),  # 5
    ]

    # Insert the dates of completion in the database (with the correct method)
    for date in dates:
        clean_db.insert_completion_datetime(habit_id, date[0])

    # Get the longest streak
    longest_streak = analytics.get_longest_streak_for_habit(habit_id)

    # The longest streak should be 5 days.
    assert longest_streak == 5, f"Expected longest streak to be 5, but got {longest_streak}"

#18 Calculate the longest streak for a particular weekly habit, passing as an argument the id of the habit.

def test_get_longest_streak_for_habit_weekly(clean_db):
    """Verify that the function correctly returns the longest streak for a weekly habit with different days of the week."""
    analytics = Analytics(db=clean_db)
    habit_manager = HabitManager()

    # Create a new habit on a weekly basis
    habit_manager.create_habit("Read a book", "weekly")
    habit_id = clean_db.get_habits()[0][0]  # Get the ID of the habit created

    # Dates simulating an interrupted streak on different days of the week
    dates = [
        ("2025-01-02 08:00:00",),  #1
        ("2025-01-09 09:00:00",),  #2
        ("2025-01-15 10:00:00",),  #3
        ("2025-01-22 08:00:00",),  #4
        # Interruption: Week of 29 January is not recorded.
        ("2025-02-06 22:00:00",),  #1
        ("2025-02-14 08:30:00",),  #2
        ("2025-02-20 07:00:00",),  #3
        ("2025-02-27 08:00:00",),  #4
        ("2025-03-05 08:00:00",),  #5
    ]
    # Insert the dates of completion in the database
    for date in dates:
        clean_db.insert_completion_datetime(habit_id, date[0])

    # Get the longest streak
    longest_streak = analytics.get_longest_streak_for_habit(habit_id)

    # The longest streak should be 5 weeks.
    assert longest_streak == 5, f"Expected longest streak to be 5, but got {longest_streak}"

#19
def test_get_longest_streak(clean_db):
    """Verify that the function returns the longest streak among all stored habits."""
    analytics = Analytics(db=clean_db)
    habit_manager = HabitManager()

    # Create several habits with different periodicities
    habit_manager.create_habit("Morning Run", "daily")
    habit_manager.create_habit("Meditation", "daily")
    habit_manager.create_habit("Read a book", "weekly")

    # Get the IDs of the created habits
    habits = clean_db.get_habits()
    habit_ids = {habit[1]: habit[0] for habit in habits}

    # Dates for the ‘Morning Run’ habit (longest streak: 4 days)
    morning_run_dates = [
        ("2025-02-01 07:00:00",),
        ("2025-02-02 07:00:00",),
        ("2025-02-03 07:00:00",),
        ("2025-02-04 07:00:00",),  #4
        # Break
        ("2025-02-06 07:00:00",),
    ]

    # Dates for the ‘Meditation’ habit (longest streak: 3 days)
    meditation_dates = [
        ("2025-02-05 08:00:00",),
        ("2025-02-06 08:00:00",),
        ("2025-02-07 08:00:00",),  #3
        # break
        ("2025-02-09 08:00:00",),
    ]

    # Dates for the habit ‘Read a book’ (weekly, longest streak: 5 weeks)
    read_book_dates = [
        ("2025-01-01 09:00:00",),  #1
        ("2025-01-08 09:00:00",),  #2
        ("2025-01-15 09:00:00",),  #3
        ("2025-01-22 09:00:00",),  #4
        ("2025-01-29 09:00:00",),  #5
        #Break
        ("2025-02-12 09:00:00",),
    ]

    # Insert dates in the database
    for date in morning_run_dates:
        clean_db.insert_completion_datetime(habit_ids["Morning Run"], date[0])

    for date in meditation_dates:
        clean_db.insert_completion_datetime(habit_ids["Meditation"], date[0])

    for date in read_book_dates:
        clean_db.insert_completion_datetime(habit_ids["Read a book"], date[0])

    # To obtain the longest streak of all habits
    longest_streak = analytics.get_longest_streak()

    # The longest streak should be 5 weeks (from ‘Read a book’).
    assert longest_streak == 5, f"Expected longest streak to be 5, but got {longest_streak}"





