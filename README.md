# Habit Tracker CLI

A simple Command-Line Interface (CLI) application to help you track your habits, monitor progress, and gain insights into your routines.

## Features

- **Interactive Menu:** Easy-to-navigate CLI with intuitive prompts.
- **Habit Management:** Add daily or weekly habits.
- **Completion Tracking:** Mark habits as complete with date tracking.
- **Analytics:** View longest streaks, habits by periodicity and more..

## Technologies Used

- **Python** with the questionary library.
- **SQLite3** for lightweight, local data storage.

## Database Structure

- **Habits:** Stores habit details (name, periodicity, user association).
- **Completions:** Tracks when habits are marked as complete (id, habit name, completion date).

## Installation

1. **Clone the Repository:**  
   ```bash
   git clone https://github.com/Nicolas-Bury/habit-tracker.git
   cd habit-tracker
   ```

2. **Install Dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```

> **Note**: It's recommended to use a virtual environment to manage dependencies. For more information, you can refer to the following resources:
> - [Python Documentation on Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## Usage

Run the application with:
```bash
python main.py
```

Follow the interactive menu to:
- Add new habits
- Mark habits as complete
- View your habits and analytics

## Example
```bash
$ python main.py

Choose an option: (Use arrow keys)
Create new habit
Delete habit
Add habit completion
Remove habit completion
Analytics Module
Exit
```

## Tests

```bash
pytest .
```

## Requirements (see requirements.txt)

- Python 3.7 or higher
- questionary library
- Pytest library

## Future Improvements

- Add support for monthly habits
- Implement a GUI