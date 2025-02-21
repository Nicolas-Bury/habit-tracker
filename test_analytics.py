import os
from datetime import datetime
import db_handler as db
import analytics

class TestAnalytics:
    test_db = "test_habit.db"

    def setup_method(self):
        """Setup a fresh test database before each test."""
        db.initialize_db(self.test_db)

        db.add_habit("Exercise", "daily", datetime(2025, 1, 1).date(), self.test_db)
        db.add_habit("Brush teeth", "daily", datetime(2025, 1, 1).date(), self.test_db)
        db.add_habit("Read", "weekly", datetime(2025, 1, 1).date(), self.test_db)
        db.add_habit("Check mails", "weekly", datetime(2025, 1, 1).date(), self.test_db)

        db.add_completion_date("Exercise", datetime(2025, 1, 1).date(), self.test_db)
        db.add_completion_date("Exercise", datetime(2025, 1, 2).date(), self.test_db)
        db.add_completion_date("Exercise", datetime(2025, 1, 3).date(), self.test_db)
        db.add_completion_date("Exercise", datetime(2025, 1, 5).date(), self.test_db)

        db.add_completion_date("Brush teeth", datetime(2025, 1, 5).date(), self.test_db)

        db.add_completion_date("Read", datetime(2025, 1, 1).date(), self.test_db)
        db.add_completion_date("Read", datetime(2025, 1, 9).date(), self.test_db)
        db.add_completion_date("Read", datetime(2025, 1, 22).date(), self.test_db)

        db.add_completion_date("Check mails", datetime(2025, 1, 22).date(), self.test_db)


    def teardown_method(self):
        """Clean up the test database after each test."""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_fetch_all_habits(self):
        """Test fetching all habits from the database."""
        habits = analytics.fetch_all_habits(db_name="test_habit.db")
        assert len(habits) == 4
        assert habits[1] == ("Exercise", "daily", datetime(2025, 1, 1).strftime('%Y-%m-%d'))
        assert habits[0] == ("Brush teeth", "daily", datetime(2025, 1, 1).strftime('%Y-%m-%d'))
        assert habits[3] == ("Read", "weekly", datetime(2025, 1, 1).strftime('%Y-%m-%d'))
        assert habits[2] == ("Check mails", "weekly", datetime(2025, 1, 1).strftime('%Y-%m-%d'))
    
    def test_fetch_daily_habits(self):
        """Test fetching daily habits from the database."""
        habits = analytics.fetch_daily_habits(db_name="test_habit.db")
        assert len(habits) == 2
        assert habits[1] == ("Exercise", "daily", datetime(2025, 1, 1).strftime('%Y-%m-%d'))
        assert habits[0] == ("Brush teeth", "daily", datetime(2025, 1, 1).strftime('%Y-%m-%d'))
    
    def test_fetch_weekly_habits(self):
        """Test fetching weekly habits from the database."""
        habits = analytics.fetch_weekly_habits(db_name="test_habit.db")
        assert len(habits) == 2
        assert habits[1] == ("Read", "weekly", datetime(2025, 1, 1).strftime('%Y-%m-%d'))
        assert habits[0] == ("Check mails", "weekly", datetime(2025, 1, 1).strftime('%Y-%m-%d'))

    def test_count_habits(self):
        """Test counting the number of habits in the database."""
        assert analytics.count_habits(db_name="test_habit.db") == 4
    
    def test_count_daily_habits(self):
        """Test counting the number of daily habits in the database."""
        assert analytics.count_daily_habits(db_name="test_habit.db") == 2

    def test_count_weekly_habits(self):
        """Test counting the number of weekly habits in the database."""
        assert analytics.count_weekly_habits(db_name="test_habit.db") == 2

    def test_fetch_habit_completion_dates(self):
        """Test fetching the completion dates of a habit from the database."""
        dates = analytics.fetch_habit_completion_dates("Exercise", db_name="test_habit.db")
        assert len(dates) == 4
        assert dates[0] == datetime(2025, 1, 1)
        assert dates[1] == datetime(2025, 1, 2)
        assert dates[2] == datetime(2025, 1, 3)
        assert dates[3] == datetime(2025, 1, 5)

        dates = analytics.fetch_habit_completion_dates("Read", db_name="test_habit.db")
        assert len(dates) == 3
        assert dates[0] == datetime(2025, 1, 1)
        assert dates[1] == datetime(2025, 1, 9)
        assert dates[2] == datetime(2025, 1, 22)
    
    def test_fetch_habit_periodicity(self):
        """Test fetching the periodicity of a habit from the database."""
        assert analytics.fetch_habit_periodicity("Exercise", db_name="test_habit.db") == "daily"
        assert analytics.fetch_habit_periodicity("Read", db_name="test_habit.db") == "weekly"
    
    def test_get_habit_longuest_streak(self):
        """Test getting the longest streak of a habit."""
        assert analytics.get_habit_longest_streak("Exercise", db_name="test_habit.db") == 3
        assert analytics.get_habit_longest_streak("Read", db_name="test_habit.db") == 2
        assert analytics.get_habit_longest_streak("Brush teeth", db_name="test_habit.db") == 1
        assert analytics.get_habit_longest_streak("Check mails", db_name="test_habit.db") == 1

    def test_get_habit_with_longest_daily_streak(self):
        """Test getting the habit with the longest daily streak."""
        assert analytics.get_habit_with_longest_daily_streak(db_name="test_habit.db") == ("Exercise", 3)
    
    def test_get_habit_with_longest_weekly_streak(self):
        """Test getting the habit with the longest weekly streak."""
        assert analytics.get_habit_with_longest_weekly_streak(db_name="test_habit.db") == ("Read", 2)

    def test_get_daily_habits_completion_ratio(self):
        """Test calculating the completion ratio for daily habits."""

        ratios = analytics.get_daily_habits_completion_ratio(db_name="test_habit.db")

        today = datetime.now()
        time_passed = (today - datetime(2025, 1, 1)).days +1

        exercise_ratio = 4 / time_passed
        brush_teeth_ratio = 1 / time_passed

        assert len(ratios) == 2
        assert ratios[1] == ("Exercise", exercise_ratio)
        assert ratios[0] == ("Brush teeth", brush_teeth_ratio)

    def test_get_weekly_habits_completion_ratio(self):
        """Test calculating the completion ratio for weekly habits."""

        ratios = analytics.get_weekly_habits_completion_ratio(db_name="test_habit.db")

        today = datetime.now()
        time_passed = ((today - datetime(2025, 1, 1)).days // 7) +1

        read_ratio = 3 / time_passed
        check_mails_ratio = 1 / time_passed

        assert len(ratios) == 2
        assert ratios[0] == ("Check mails", check_mails_ratio)
        assert ratios[1] == ("Read", read_ratio)
