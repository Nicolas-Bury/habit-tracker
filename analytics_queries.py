all_habits_query = """
    SELECT * 
    FROM habits 
    ORDER BY periodicity ASC, creation_date ASC, habit ASC
    """ 
daily_habits_query = """
    SELECT * 
    FROM habits 
    WHERE periodicity = 'daily' 
    ORDER BY habit ASC
    """
weekly_habits_query = """
    SELECT * 
    FROM habits 
    WHERE periodicity = 'weekly' 
    ORDER BY habit ASC
    """
count_habits_query = """
    SELECT COUNT(*) 
    FROM habits
    """
count_daily_habits_query = """
    SELECT COUNT(*) 
    FROM habits
    WHERE periodicity = 'daily'
    """
count_weekly_habits_query = """
    SELECT COUNT(*) 
    FROM habits
    WHERE periodicity = 'weekly'
    """

habit_completion_dates_query = """
    SELECT completion_date
    FROM completions
    WHERE habit = ?
    ORDER BY completion_date
    """

habit_periodicity_query = """
    SELECT periodicity
    FROM habits
    WHERE habit = ?
    """