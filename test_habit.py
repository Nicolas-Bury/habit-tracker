import os
from datetime import date
import db_handler as db
from habit import Habit
import pytest

class TestHabit:
    test_db = "test_habit.db"

    def setup_method(self):
        """Setup a fresh test database before each test."""
        db.initialize_db(self.test_db)

    def teardown_method(self):
        """Clean up the test database after each test."""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_habit_creation(self):
        """Test if a habit is correctly initialized."""
        habit = Habit("Exercise", "daily")
        assert habit.habit == "Exercise"
        assert habit.periodicity == "daily"
        assert isinstance(habit.creation_date, date)

    def test_invalid_habit_name(self):
        """Test if a habit name is invalid."""
        with pytest.raises(ValueError, match="Habit name must be at least 3 characters long."):
            Habit("Ex", "daily")
        
        with pytest.raises(ValueError, match="Habit name must be at most 20 characters long."):
            Habit("E" * 21, "daily")

    def test_invalid_habit_periodicity(self):
        """Test that an invalid periodicity raises a ValueError."""
        with pytest.raises(ValueError, match="Periodicity must be either 'daily' or 'weekly'."):
            Habit("Exercise", "monthly")

        with pytest.raises(ValueError, match="Periodicity must be either 'daily' or 'weekly'."):
            Habit("Exercise", "")

    def test_save_habit(self):
        """Test saving a habit in the database."""
        habit = Habit("Exercise", "daily")
        habit.save(self.test_db)
        assert Habit.exists("Exercise", self.test_db)

    def test_remove_habit(self):
        """Test removing a habit from the database."""
        habit = Habit("Exercise", "daily")
        habit.save(self.test_db)
        Habit.remove("Exercise", self.test_db)
        assert not Habit.exists("Exercise", self.test_db)

    def test_add_completion_date(self):
        """Test adding a habit completion date."""
        habit = Habit("Exercise", "daily")
        habit.save(self.test_db)
        Habit.add_completion_date("Exercise", date.today(), self.test_db)
        assert Habit.completion_date_exists("Exercise", date.today(), self.test_db)

    def test_remove_completion_date(self):
        """Test removing a habit completion date."""
        habit = Habit("Exercise", "daily")
        habit.save(self.test_db)
        Habit.add_completion_date("Exercise", date.today(), self.test_db)
        Habit.remove_completion_date("Exercise", date.today(), self.test_db)
        assert not Habit.completion_date_exists("Exercise", date.today(), self.test_db)