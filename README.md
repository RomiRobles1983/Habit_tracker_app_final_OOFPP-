# Habit Tracker CLI

## Description

Habit Tracker CLI is a command-line interface application for managing and tracking habits. It allows users to create, delete, mark as completed, and track streaks of various habits. This tool helps users stay consistent with their daily or weekly goals by providing insights into their longest streaks.

## Features  
Habit Tracker CLI is a command-line application that helps users track their daily and weekly habits efficiently. Users can create, complete, analyze, and delete habits while keeping track of their longest streaks.

- Create daily and weekly habits
- Delete registered habits
- Mark habits as completed with a specific date and time
- List all habits or filter them by periodicity (daily/weekly)
- Retrieve the longest streak of all habits
- Retrieve the longest streak of a specific habit
- Load predefined habits for quick setup

## How it works  
- Create a habit: Users define a habit with a name and periodicity (daily or weekly).
- Complete a habit: When a user performs a habit, they mark it as completed with a timestamp.
- Track progress: Users can view their list of habits and analyze streaks.
- Analyze habits: The system calculates the longest streaks for individual habits and overall.
- Manage habits: Users can delete habits if they no longer need them.

- Bonus: Users can load predefined habits from a JSON file for quick setup.

## Installation

To install and set up the Habit Tracker CLI, follow these steps:

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/RomiRobles1983/habit-tracker
    ```

2. Navigate to the project directory:
    ```bash
    cd habit-tracker
    ```

3. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv env
    ```

4. Activate the virtual environment:
    - On Windows:
        ```bash
        .\env\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source env/bin/activate
        ```

5. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Start the Command-Line Interface (CLI)

To run the Habit Tracker CLI, use the following command:
```bash
python main.py
```
### Available Commands
1-Create: Creates a new habit with the specified name and periodicity (daily/weekly).
```bash
create <name> <periodicity>
    python main.py create "Meditate" "daily"
```
2-Complete: Marks a habit as completed with a manually entered date and time in the format YYYY-MM-DD HH:MM:SS.
```bash
complete <habit_id> <datetime_str>
    python main.py complete 1 "2025-01-01 10:00:00"
```
3-Delete: Deletes a habit by its ID
```bash
delete <habit_id>
    python main.py delete 1
```
4-List-habits: Lists all current habits.
```bash
    python main.py list_habits
```
5-List-by-periodicity: Lists all habits with a specific periodicity (daily or weekly).
```bash
list-by-periodicity <periodicity>
    python main.py list-by-periodicity daily
```
6-Longest-streak: Shows the longest streak across all habits.
```bash
    python main.py longest_streak
```
7-Streak: Retrieves the longest streak of a specific habit.
```bash
streak <habit_id>
    python main.py longest-streak-per-habit 50
```
8-Load-predefined-habits: Deletes existing habits and loads predefined habits from a JSON file.
```bash
    python main.py load-predefined-habits
    
```
### Testing
The test cases for the Habit Tracker CLI are located in the test_habit_tracker.py file.
To run the tests, execute the following command:
```bash
    pytest test_habit_tracker.py
    
```
## Data Persistence

Habit Tracker CLI stores habit data in an **SQLite database (`habits.db`)**, ensuring data is saved across sessions.

- Each habit consists of:
  - A **name** (e.g., "Exercise")
  - A **periodicity** (`daily` or `weekly`)
  - A list of **completion timestamps**, which track when the habit was marked as completed.

- **Completion records** allow the application to accurately compute habit streaks, ensuring users can track their consistency.

- The **`load-predefined-habits`** command:
  - Deletes all existing habits and their completion records.
  - Loads a predefined set of habits from a JSON file for quick setup.