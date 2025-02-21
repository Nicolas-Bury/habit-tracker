import sqlite3
from datetime import date
from datetime import datetime

def connect_db(db_name: str = "habit.db") -> sqlite3.Connection: # default value to be removed if not used in pytest & analytics
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

def initialize_db(db_name: str) -> None:
    """
    Creates the 'habits' and 'completions' tables in the SQLite database if they do not already exist.

    Args:
        db_name (str): The name of the database file to initialize.
    """
    try:
        con, cursor = connect_db(db_name)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                habit TEXT PRIMARY KEY,
                periodicity TEXT CHECK(periodicity IN ('daily', 'weekly')) NOT NULL,
                creation_date TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit TEXT NOT NULL,
                completion_date TEXT NOT NULL,
                FOREIGN KEY(habit) REFERENCES habits(habit) ON DELETE CASCADE,
                UNIQUE (habit, completion_date)
            )
        """)
        con.commit()
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()

def add_habit(habit: str, periodicity: str, creation_date: date, db_name: str) -> None:
    """
    Adds a new habit to the database.

    Args:
        habit (str): The name of the habit to be added.
        periodicity (str): The periodicity of the habit ('daily' or 'weekly').
        creation_date (date): The date the habit was created.
        db_name (str): The name of the database file.
    """
    try:
        con, cursor = connect_db(db_name)
        cursor.execute("""
            INSERT INTO habits (habit, periodicity, creation_date)
            VALUES (?, ?, ?)                
        """, (habit, periodicity, creation_date))
        con.commit()
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()

def remove_habit(habit: str, db_name: str) -> None:
    """
    Removes a habit from the database.

    Args:
        habit (str): The name of the habit to be removed.
        db_name (str): The name of the database file.
    """
    try:
        con, cursor = connect_db(db_name)
        cursor.execute("""
            DELETE FROM habits
            WHERE habit = ?               
        """, (habit,))
        con.commit()
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()

def habit_exists(habit: str, db_name: str) -> bool:
    """
    Checks if a specific habit exists in the database.

    Args:
        habit (str): The name of the habit to check.
        db_name (str): The name of the database file.

    Returns:
        bool: True if the habit exists, False otherwise.
    """
    try:
        con, cursor = connect_db(db_name)
        cursor.execute("""
            SELECT 1 FROM habits WHERE habit = ?              
        """, (habit,))
        result = cursor.fetchone()
        return result is not None
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()

def add_completion_date(habit: str, date: date, db_name: str) -> None:
    """
    Adds a completion date for a habit in the database.

    Args:
        habit (str): The name of the habit.
        date (date): The completion date.
        db_name (str): The name of the database file.
    """
    try:
        con, cursor = connect_db(db_name)
        cursor.execute("""
            INSERT INTO completions (habit, completion_date)
            VALUES (?, ?)               
        """, (habit, date.isoformat()))
        con.commit()
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()

def remove_completion_date(habit: str, date: date, db_name: str) -> None:
    """
    Remove a habit completion date in the db

    Args:
        habit (str): The name of the habit.
        date (date): The completion date.
        db_name (str): The name of the database file.
    """
    try:
        con, cursor = connect_db(db_name)
        cursor.execute("""
            DELETE FROM completions
            WHERE habit = ? AND completion_date = ?            
        """, (habit, date.isoformat()))
        con.commit()
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()

def completion_date_exists(habit: str, date: date, db_name: str) -> bool:
    """
    Checks if a habit's completion date exists in the database.

    Args:
        habit (str): The name of the habit.
        date (date): The completion date to check.
        db_name (str): The name of the database file.

    Returns:
        bool: True if the completion date exists, False otherwise.
    """
    try:
        con, cursor = connect_db(db_name)
        cursor.execute("""
            SELECT 1 FROM completions WHERE habit = ? AND completion_date = ?              
        """, (habit, date.isoformat()))
        result = cursor.fetchone()
        return result is not None
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()

def completion_week_exists(habit: str, date: date, db_name: str) -> bool:
    """
    Checks if a weekly habit was already completed during the same week.

    Args:
        habit (str): The name of the habit.
        date (date): The completion date to check.
        db_name (str): The name of the database file.

    Returns:
        bool: True if the habit was completed during the same week, False otherwise.
    """
    try:
        con, cursor = connect_db(db_name)
        cursor.execute("""
            SELECT completion_date FROM completions WHERE habit = ?             
        """, (habit,))
        dates = cursor.fetchall()
        for d in dates:
            year, week, _ = datetime.strptime(d[0], "%Y-%m-%d").isocalendar()
            if date.isocalendar()[:2] == (year, week):
                return True
        return False
    except sqlite3.Error as e:
        print(f"database error: {e}")
    finally:
        con.close()
