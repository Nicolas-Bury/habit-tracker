from datetime import date
import db_handler as db

class Habit:
    """
    A class to represent a habit.

    Attributes:
        habit (str): The name of the habit.
        periodicity (str): The periodicity of the habit ('daily' or 'weekly').
        creation_date (date): The date when the habit was created.
    """

    def __init__(self, habit: str, periodicity: str) -> None:
        """
        Constructs all the necessary attributes for the Habit object and save the habit to the database.

        Args:
            habit (str): The name of the habit (3 to 20 characters long).
            periodicity (str): The periodicity of the habit ('daily' or 'weekly').
        
        Attributes:
            creation_date (date): The date when the habit was created.
        """
        if periodicity not in ['daily', 'weekly']:
            raise ValueError("Periodicity must be either 'daily' or 'weekly'.")
        
        if len(habit) < 3:
            raise ValueError("Habit name must be at least 3 characters long.")
        elif len(habit) > 20:
            raise ValueError("Habit name must be at most 20 characters long.")
        
        self.habit = habit
        self.periodicity = periodicity
        self.creation_date = date.today()

    def __str__(self) -> str:
        """
        Returns a string representation of the Habit object.

        Returns:
            str: A formatted string containing the habit name and creation date.
        """
        return f"{self.habit} (created on {self.creation_date})"

    def save(self, db_name: str = "habit.db") -> None:
        """
        Save a habit to the database.
        
        Args:
            db_name (str, optional): The name of the database file. Defaults to 'habit.db'.
        """
        db.add_habit(self.habit, self.periodicity, self.creation_date, db_name)
    
    @staticmethod
    def remove(habit: str, db_name: str = "habit.db") -> None:
        """
        Remove a habit from the database.
        
        Args:
            habit (str): The name of the habit to remove.
            db_name (str, optional): The name of the database file. Defaults to "habit.db".
        """
        db.remove_habit(habit, db_name)

    @staticmethod
    def exists(habit: str, db_name: str = "habit.db") -> bool:
        """
        Check if a habit already exists in the database.
        
        Args:
            habit (str): The name of the habit to check.
            db_name (str, optional): The name of the database file. Defaults to "habit.db".
        
        Returns:
            bool: True if the habit already exists, False otherwise.
        """
        return db.habit_exists(habit, db_name)

    @staticmethod
    def add_completion_date(habit: str, date: date, db_name: str = "habit.db") -> None:
        """
        Add a habit completion date in the database.
        
        Args:
            habit (str): The name of the habit.
            date (date): The completion date to be recorded.
            db_name (str, optional): The name of the database file. Defaults to "habit.db".
        """
        db.add_completion_date(habit, date, db_name)

    @staticmethod
    def remove_completion_date(habit: str, date: date, db_name: str = "habit.db") -> None:
        """
        Removes a habit completion date from the database.

        Args:
            habit (str): The name of the habit.
            date (date): The completion date to be removed.
            db_name (str, optional): The name of the database file. Defaults to "habit.db".
        """
        db.remove_completion_date(habit, date, db_name)

    @staticmethod
    def completion_date_exists(habit: str, date: date, db_name: str = "habit.db") -> bool:
        """
        Checks if a completion date already exists in the database.

        Args:
            habit (str): The name of the habit.
            date (date): The completion date to check.
            db_name (str, optional): The name of the database file. Defaults to "habit.db".

        Returns:
            bool: True if the completion date exists, False otherwise.
        """
        return db.completion_date_exists(habit, date, db_name)
    
    @staticmethod
    def completion_week_exists(habit: str, date: date, db_name: str = "habit.db") -> bool:
        """
        Checks if a weekly habit was already completed during the same week.

        Args:
            habit (str): The name of the habit.
            date (date): The date to check for weekly completion.
            db_name (str, optional): The name of the database file. Defaults to "habit.db".

        Returns:
            bool: True if the habit was completed that week, False otherwise.
        """
        return db.completion_week_exists(habit, date, db_name)
    