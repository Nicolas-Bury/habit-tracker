import sqlite3
from datetime import datetime, timedelta
from analytics_queries import *

def connect_db(db_name: str = "habit.db") -> sqlite3.Connection:
    """
    Establishes a connection to the SQLite database and enables foreign key constraints.

    Args:
        db_name (str, optional): The name of the database file. Defaults to "habit.db".

    Returns:
        sqlite3.Connection: A connection object to interact with the database.
    """
    con = sqlite3.connect(db_name)
    con.execute("PRAGMA foreign_keys = ON")
    return con, con.cursor()

def fetch_all_habits(db_name: str = "habit.db") -> list[tuple]:
    """
    Fetch all habits from the database.
    
    Args:
        db_name (str, optional): The name of the database file. Defaults to "habit.db".
    
    Returns:
        list[tuple]: A list of tuples containing the habit name, periodicity, and creation date.
    """
    con, cursor = connect_db(db_name)
    try:
        return cursor.execute(all_habits_query).fetchall()
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()

def fetch_daily_habits(db_name: str = "habit.db") -> list[tuple]:
    """
    Fetch all daily habits from the database.
    
    Args:
        db_name (str, optional): The name of the database file. Defaults to "habit.db".
    
    Returns:
        list[tuple]: A list of tuples containing the habit name, periodicity, and creation date.
    """
    con, cursor = connect_db(db_name)
    try:
        return cursor.execute(daily_habits_query).fetchall()
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()

def fetch_weekly_habits(db_name: str = "habit.db") -> list[tuple]:
    """
    Fetch all weekly habits from the database.
    
    Args:
        db_name (str, optional): The name of the database file. Defaults to "habit.db".
    
    Returns:
        list[tuple]: A list of tuples containing the habit name, periodicity, and creation date.
    """
    con, cursor = connect_db(db_name)
    try:
        return cursor.execute(weekly_habits_query).fetchall()
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()

def count_habits(db_name: str = "habit.db") -> int:
    """
    Returns the total number of habits in the database.

    Args:
        db_name (str, optional): The name of the database file. Defaults to "habit.db".

    Returns:
        int: The total number of habits in the database.
    """
    con, cursor = connect_db(db_name)
    try:
        cursor.execute(count_habits_query)
        return cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()

def count_daily_habits(db_name: str = "habit.db") -> int:
    """
    Returns the total number of daily habits in the database.

    Args:
        db_name (str, optional): The name of the database file. Defaults to "habit.db".

    Returns:
        int: The total number of daily habits in the database.
    """
    con, cursor = connect_db(db_name)
    try:
        cursor.execute(count_daily_habits_query)
        return cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()

def count_weekly_habits(db_name: str = "habit.db") -> int:
    """
    Returns the total number of habits in the database.

    Args:
        db_name (str, optional): The name of the database file. Defaults to "habit.db".

    Returns:
        int: The total number of weekly habits in the database.
    """
    con, cursor = connect_db(db_name)
    try:
        cursor.execute(count_weekly_habits_query)
        return cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()

def fetch_habit_completion_dates(habit_name: str, db_name: str = "habit.db") -> list[datetime]:
    """
    Fetch all completion dates for a specific habit.

    Args:
        habit_name (str): The name of the habit.
        db_name (str, optional): The name of the database file. Defaults to "habit.db".
    
    Returns:
        list[datetime]: A list of datetime objects representing the completion dates.
    """
    con, cursor = connect_db(db_name)
    try:
        cursor.execute(habit_completion_dates_query, (habit_name,))
        data = cursor.fetchall() # returns a list of tuples with dates as strings
        return [datetime.strptime(date[0], "%Y-%m-%d") for date in data] # convert strings to datetime objects
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()

def fetch_habit_periodicity(habit_name: str, db_name: str = "habit.db") -> str:
    """
    Fetch the periodicity of a specific habit.

    Args:
        habit_name (str): The name of the habit.
        db_name (str, optional): The name of the database file. Defaults to "habit.db".
    
    Returns:
        str: The periodicity of the habit ('daily' or 'weekly').
    """
    con, cursor = connect_db(db_name)
    try:
        cursor.execute(habit_periodicity_query, (habit_name,))
        return cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()

def calculate_daily_streak(dates: list) -> int:
    """
    Calculate the longest streak of days for a list of given dates.
    
    Args:
        dates (list): A list of datetime objects representing the completion dates of the habit.
    
    Returns:
        int: The longest streak of consecutive days in the provided list of dates.
    """
    if not dates:
        return 0

    longest_streak = 1
    current_streak = 1

    for i in range(1, len(dates)):
        if dates[i] - dates[i - 1] == timedelta(days=1):
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1

    return max(longest_streak, current_streak)

def calculate_weekly_streak(dates: list) -> int:
    """
    Calculate the longest streak of weeks for a given list of dates.
    
    Args:
        dates (list): A list of datetime objects representing the completion dates of the habit.
    
    Returns:
        int: The longest streak of consecutive weeks in the provided list of dates.
    """
    if not dates:
        return 0

    longest_streak = 1
    current_streak = 1

    for i in range(1, len(dates)):
        prev_year, prev_week, _ = dates[i - 1].isocalendar()
        current_year, current_week, _ = dates[i].isocalendar()
        if current_year == prev_year and current_week == prev_week: 
            # should not happen anymore with the new completion_week_exists function, but keep to be safe
            continue
        elif current_year == prev_year and current_week == prev_week + 1:
            current_streak += 1
        elif current_year == prev_year + 1 and prev_week == 52 and current_week == 1:
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1

    return max(longest_streak, current_streak)

def get_habit_longest_streak(habit_name: str, db_name: str = "habit.db") -> int:
    """
    Main function to get the longest streak for a selected habit, either daily or weekly based on the habit periodicity.
    
    Args:
        habit_name (str): The name of the habit.
        db_name (str, optional): The name of the database file. Defaults to "habit.db".

    Returns:
        int: The longest streak of completions ('daily' or 'weekly') for the selected habit.
    """
    periodicity = fetch_habit_periodicity(habit_name, db_name)
    if not periodicity:
        return 0
    
    dates = fetch_habit_completion_dates(habit_name, db_name)
    if not dates:
        return 0
    
    if periodicity == "daily":
        return calculate_daily_streak(dates)
    elif periodicity == "weekly":
        return calculate_weekly_streak(dates)
    else:
        print("Unknown periodicity")
        return 0

def get_habit_with_longest_daily_streak(db_name: str = "habit.db") -> list[str, int]:
    """
    Get the habit with the longest daily streak.

    Args:
        db_name (str, optional): The name of the database file. Defaults to "habit.db".
    
    Returns:
        list[str, int]: A list containing the habit name and the longest daily streak.
    """
    habits = fetch_all_habits(db_name)
    longest_daily_streak = ("", 0)
    
    for habit_name, periodicity, _ in habits:
        if periodicity == "daily":
            streak = get_habit_longest_streak(habit_name, db_name)
            if streak > longest_daily_streak[1]:
                longest_daily_streak = (habit_name, streak)
    
    return longest_daily_streak

def get_habit_with_longest_weekly_streak(db_name: str = "habit.db") -> list[str, int]:
    """
    Get the habit with the longest weekly streak.

    Args:
        db_name (str, optional): The name of the database file. Defaults to "habit.db".
    
    Returns:
        list[str, int]: A list containing the habit name and the longest weekly streak.
    """
    habits = fetch_all_habits(db_name)
    longest_weekly_streak = ("", 0)
    
    for habit_name, periodicity, _ in habits:
        if periodicity == "weekly":
            streak = get_habit_longest_streak(habit_name, db_name)
            if streak > longest_weekly_streak[1]:
                longest_weekly_streak = (habit_name, streak)
    return longest_weekly_streak

def get_daily_habits_completion_ratio(db_name: str = "habit.db") -> list[tuple[str, float]]:
    """
    Get the completion ratio for all daily habits.
    e.g. a habit is completed 4x in a period of 10 days, the completion ratio is 4/10 = 40%
    
    Args:
        db_name (str, optional): The name of the database file. Defaults to "habit.db".
    
    Returns:
        list[str, float]: A list of tuples containing the habit name and the completion ratio.
    """
    habits = fetch_daily_habits(db_name)
    completion_ratios = []

    for habit, _, creation_date in habits:
        creation_date = datetime.strptime(creation_date, "%Y-%m-%d")
        today = datetime.now()
        habit_length = (today - creation_date).days
        completion_occurences = len(fetch_habit_completion_dates(habit, db_name))
        completion_ratio = completion_occurences / habit_length if habit_length > 0 else 0
        completion_ratios.append((habit, completion_ratio))
    return completion_ratios

def get_weekly_habits_completion_ratio(db_name: str = "habit.db") -> list[tuple[str, float]]:
    """
    Get the completion ratio for all weekly habits.
    e.g. a habit is completed 4x in a period of 10 weeks, the completion ratio is 4/10 = 40%
    
    Args:
        db_name (str, optional): The name of the database file. Defaults to "habit.db".
    
    Returns:
        list[str, float]: A list of tuples containing the habit name and the completion ratio.
    """
    habits = fetch_weekly_habits(db_name)
    completion_ratios = []

    for habit, _, creation_date in habits:
        creation_date = datetime.strptime(creation_date, "%Y-%m-%d")
        today = datetime.now()
        habit_length = (today - creation_date).days // 7
        completion_occurences = len(fetch_habit_completion_dates(habit, db_name))
        completion_ratio = completion_occurences / habit_length if habit_length > 0 else 0
        completion_ratios.append((habit, completion_ratio))
    return completion_ratios
