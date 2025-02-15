from db_manager import HabitDatabase
from datetime import datetime, timedelta


class Analytics:
    """
    A class responsible for analyzing habits, such as calculating streaks.
    """

    def __init__(self, db=None):
        """
        Initialize the Analytics class with a connection to the HabitDatabase.
        If no database is provided, it will create a default HabitDatabase instance.

        Args:
            db (HabitDatabase, optional): The database instance. Defaults to None.
        """
        self.db = db if db else HabitDatabase()  # If no db is passed, use HabitDatabase()

    def get_longest_streak(self):
        """
        Calculate the longest streak across all habits.

        Returns:
            int: The length of the longest streak in days or weeks, depending on the habit periodicity.
        """
        habits = self.db.get_habits()
        longest_streak = 0

        for habit in habits:
            habit_id = habit[0]
            periodicity = habit[2]  # Get the periodicity of the habit
            completion_dates = self.db.get_completion_dates(habit_id)
            streak = self._calculate_streak(completion_dates, periodicity)
            longest_streak = max(longest_streak, streak)

        return longest_streak

    def get_longest_streak_for_habit(self, habit_id):
        """
        Calculate the longest streak for a specific habit.

        Args:
            habit_id (int): The ID of the habit.

        Returns:
            int: The length of the longest streak in days or weeks, depending on the habit periodicity.
        """
        habit = self.db.get_habit_by_id(habit_id)  # Get the habit by its ID
        if habit:
            periodicity = habit[2]  # Get the periodicity of the habit
            completion_dates = self.db.get_completion_dates(habit_id)
            return self._calculate_streak(completion_dates, periodicity)
        else:
            return 0  # If the habit does not exist


    def _calculate_streak(self, dates, periodicity):

        if not dates:
            return 0
    # Convert dates to just year, month and day
        dates = [datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S").date() for date in dates]
    
    # Sort dates in ascending order
        dates.sort()
        print(f"Fechas de completion: {dates}")
    
        max_streak = 1
        current_streak = 1
    
    # Scroll through the dates and compare if they are consecutive
        if periodicity == "daily":
            for i in range(1, len(dates)):
                date_diff = dates[i] - dates[i - 1]
        
        # If the difference is one day, continue the streak
                if date_diff == timedelta(days=1):
                    current_streak += 1
                else:
            # If there is a gap, restart the streak.
                    max_streak = max(max_streak, current_streak)
                    current_streak = 1

        elif periodicity == "weekly":
            last_date = dates[0]
            last_week = last_date.isocalendar()[1]
            last_year = last_date.isocalendar()[0]
        
            for i in range(1, len(dates)):
                current_date = dates[i]
                current_week, current_year = current_date.isocalendar()[1], current_date.isocalendar()[0]

            #  If the week changes, evaluate streaka
                if (current_year, current_week) > (last_year, last_week):  
                    if (current_year == last_year and current_week == last_week + 1) or \
                       (current_year > last_year and last_week == 52 and current_week == 1):
                        current_streak += 1  #Add if it is a consecutive week
                    else:
                        max_streak = max(max_streak, current_streak)
                        current_streak = 1  # Reset streak if there is an empty week

                # Update last registered week
                    last_week, last_year = current_week, current_year


    # Ensure that the latest streak is taken into account
        max_streak = max(max_streak, current_streak)
    
        return max_streak

    def close(self):
        """
        Close the database connection.
        """
        self.db.close()






