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
        print(f"Ordered completion dates: {dates}")
    
        max_streak = 1
        current_streak = 1
    
    # Scroll through the dates and compare if they are consecutive
        if periodicity == "daily":
            for i in range(1, len(dates)):
                date_diff = dates[i] - dates[i - 1]

                print(f"Comparing {dates[i-1]} → {dates[i]} | Difference: {date_diff.days} days")
        
        # If the difference is one day, continue the streak
                if date_diff == timedelta(days=1):
                    current_streak += 1
                    print(f"Continuing streak: {current_streak}")
                else:
            # If there is a gap, restart the streak.
                    max_streak = max(max_streak, current_streak)
                    print(f"Streak broken! Max so far: {max_streak}")
                    current_streak = 1
            max_streak = max(max_streak, current_streak)

        elif periodicity == "weekly":
        # Get unique weeks in format (year, week)
            weeks_with_completion = {(date.isocalendar()[0], date.isocalendar()[1]) for date in dates}
            

        # Order the weeks
            sorted_weeks = sorted(weeks_with_completion)
            

            last_year, last_week = None, None
            for year, week in sorted_weeks:
                print(f"Checking week: {year}-W{week}")
                if last_year is None:  # First week registered
                    current_streak = 1
                elif (year == last_year and week == last_week + 1) or (year > last_year and last_week == 52 and week == 1):
                    current_streak += 1  # Week in a row, add to the streak
                else:
                    max_streak = max(max_streak, current_streak)
                    current_streak = 1  # There was an empty week, restarting the streak

                last_year, last_week = year, week  # Update last registered week
                

            max_streak = max(max_streak, current_streak)
            print(f"Final max streak: {max_streak}")
        
        return max_streak

    def close(self):
        """
        Close the database connection.
        """
        self.db.close()






