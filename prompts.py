import questionary
from datetime import datetime
from habit import Habit
import analytics

def pause() -> None:
    """Makes a pause between prompts to avoid getting lost with outputs."""
    input("Press Enter to continue..\n")

def select_habit() -> str | None:
    """Prompt the user to select a habit from the list of habits."""
    if analytics.count_habits() > 0:
        habit_name = questionary.select(
            "Select the habit:",
            choices=[habit[0] for habit in analytics.fetch_all_habits()]
        ).ask()
        return habit_name
    else:
        print("There is no existing habit")
        pause()
        return None

def enter_date() -> datetime:
    """Prompts the user to enter a date with format (DD.MM.YYYY)."""
    while True:
        completion_date = questionary.text("Enter the completion date (DD.MM.YYYY):").ask()
        try:
            completion_date = datetime.strptime(completion_date, "%d.%m.%Y").date()
            return completion_date
        except ValueError:
            print("Error: Invalid date format.")
            pause()

def create_habit() -> None:
    """Prompts the users to create a habit by providing a habit name and selecting a periodicity."""
    habit_name = questionary.text("Enter the habit name:").ask()
    periodicity = questionary.select(
        "Select the habit periodicity:",
        choices=['daily', 'weekly']
    ).ask()

    if habit_name:
        if Habit.exists(habit_name):
            print(f"Habit '{habit_name}' already exists.")
        else:
            new_habit = Habit(habit_name, periodicity)
            Habit.save(new_habit)
            print(f"Habit '{habit_name}' added successfully.")
        pause()
    else:
        print("Error: Habit name is required.")
        pause()

def remove_habit() -> None:
    """Prompts the user with a list of all existing habits and asks to select the one to be removed."""
    habit_name = select_habit()
    if habit_name is not None:
        Habit.remove(habit_name)
        print(f"Habit '{habit_name}' removed successfully.")
        pause()

def add_completion_date() -> None:
    """Prompts the user with a list of existing habits and asks to enter a completion date with format (DD.MM.YYYY)."""
    habit_name = select_habit()
    periodicity = analytics.fetch_habit_periodicity(habit_name)
    if habit_name is not None:
        completion_date = enter_date()
    if periodicity == "daily" and Habit.completion_date_exists(habit_name, completion_date):
        print(f"Completion already exists for habit '{habit_name}' on {completion_date}.")
    elif periodicity == "weekly" and Habit.completion_week_exists(habit_name, completion_date):
        print(f"Completion already exists for habit '{habit_name}' on the week of {completion_date}.")
    else:
        Habit.add_completion_date(habit_name, completion_date)
        print(f"Completion added for habit '{habit_name}' on {completion_date}.")
    pause()

def remove_completion_date() -> None:
    """Prompts the user with a list of existing habits and asks to enter a completion date with format (DD.MM.YYY) he wants to remove from the DB."""
    habit_name = select_habit()
    if habit_name is not None:
        completion_date = enter_date()
    if Habit.completion_date_exists(habit_name, completion_date):
        Habit.remove_completion_date(habit_name, completion_date)
        print(f"Completion removed for habit '{habit_name}' on {completion_date}.")
    else:
        print(f"No completion found for habit '{habit_name}' on {completion_date}.")
    pause()

def view_all_habits() -> None:
    """Enables user to get access to the analytics module by calling the corresponding function."""
    habits = analytics.fetch_all_habits()
    if habits:
        for habit in habits:
            print(f" - {habit[0]} - {habit[1]} (created on {habit[2]})")
    else:
        print("No habits found.")
    pause()

def view_daily_habits() -> None:
    """Enables user to get access to the analytics module by calling the corresponding function."""
    habits = analytics.fetch_daily_habits()
    if habits:
        for habit in habits:
            print(f" - {habit[0]} (created on {habit[2]})")
    else:
        print("No daily habits found.")
    pause()

def view_weekly_habits() -> None:
    """Enables user to get access to the analytics module by calling the corresponding function."""
    habits = analytics.fetch_weekly_habits()
    if habits:
        for habit in habits:
            print(f" - {habit[0]} (created on {habit[2]})")
    else:
        print("No weekly habits found.")
    pause()

def view_habit_completion_dates() -> None:
    """Enables user to get access to the analytics module by calling the corresponding function."""
    habit_name = select_habit()
    if habit_name is not None:
        dates = analytics.fetch_habit_completion_dates(habit_name)
        if dates:
            for date in dates:
                print(f" - {date.date()}")
        else:
            print("No completion dates found.")
        pause()

def view_longest_streak_of_habit() -> None:
    """Enables user to get access to the analytics module by calling the corresponding function."""
    habit_name = select_habit()
    if habit_name is not None:
        longest_streak = analytics.get_habit_longest_streak(habit_name)
        periodicity = analytics.fetch_habit_periodicity(habit_name)
        formatted_period = (lambda x: "days" if x == "daily" else "weeks")(periodicity)
        if longest_streak == 0:
            print(f"No completion found for habit '{habit_name}'.")
        else:
            print(f"Longest streak for habit '{habit_name}': {longest_streak} {formatted_period}.")
        pause()
        
    pause()

def view_longest_streak_of_all() -> None:
    """Enables user to get access to the analytics module by calling the corresponding function."""
    if analytics.count_habits == 0:
        print("No habits found.")
    else:
        daily_streak = analytics.get_habit_with_longest_daily_streak()
        if daily_streak[1] == 0:
            print("No daily streak found.")
        weekly_streak = analytics.get_habit_with_longest_weekly_streak()
        if weekly_streak[1] == 0:
            print("No weekly streak found.")

        print(f"Longest daily streak: {daily_streak[0]} with {daily_streak[1]} days.")
        print(f"Longest weekly streak: {weekly_streak[0]} with {weekly_streak[1]} weeks.")
    pause()

def view_daily_habits_completion_ratio() -> None:
    """Enables user to get access to the analytics module by calling the corresponding function."""
    if analytics.count_daily_habits() == 0:
        print("No daily habits found.")
    else:
        ratio = analytics.get_daily_habits_completion_ratio()
        for habit, completion_ratio in ratio:
            print(f" - {habit}: {completion_ratio *100:.2f}%")
    pause()

def view_weekly_habits_completion_ratio() -> None:
    """Enables user to get access to the analytics module by calling the corresponding function."""
    if analytics.count_weekly_habits() == 0:
        print("No weekly habits found.")
    else:
        ratio = analytics.get_weekly_habits_completion_ratio()
        for habit, completion_ratio in ratio:
            print(f" - {habit}: {completion_ratio *100:.2f}%")
    pause()
