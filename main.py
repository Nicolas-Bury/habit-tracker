import questionary
import prompts
from db_handler import initialize_db

def start() -> None:
    """Main entry point for the Habit Tracker App, acting like an interactive menu for the user."""
    
    initialize_db(db_name="habit.db")

    while True:
        choice = questionary.select(
            "Choose an option:",
            choices=[
                "Create new habit",
                "Delete habit",
                "Add habit completion",
                "Remove habit completion",
                "Analytics Module",
                "Exit"
            ]
        ).ask()
        
        if choice == "Create new habit":
            prompts.create_habit()
        elif choice == "Delete habit":
            prompts.remove_habit()
        elif choice == "Add habit completion":
            prompts.add_completion_date()
        elif choice == "Remove habit completion":
            prompts.remove_completion_date()
        elif choice == "Analytics Module":
            analytics_module()
        elif choice == "Exit":
            print("Goodbye!")
            break

def analytics_module() -> None:
    """Interactive menu for the Analytics Module."""
    while True:
        choice = questionary.select(
            "Choose an option:",
            choices=[
                "View all habits",
                "View daily habits",
                "View weekly habits",
                "View habit completion dates",
                "View longuest streak of all",
                "View longuest streak of specific habit",
                "View daily habits completion ratio",
                "View weekly habits completion ratio",
                "Back"
            ]
        ).ask()
        if choice == "View all habits":
            prompts.view_all_habits()
        elif choice == "View daily habits":
            prompts.view_daily_habits()
        elif choice == "View weekly habits":
            prompts.view_weekly_habits()
        elif choice == "View habit completion dates":
            prompts.view_habit_completion_dates()
        elif choice == "View longuest streak of all":
            prompts.view_longest_streak_of_all()
        elif choice == "View longuest streak of specific habit":
            prompts.view_longest_streak_of_habit()
        elif choice == "View daily habits completion ratio":
            prompts.view_daily_habits_completion_ratio()
        elif choice == "View weekly habits completion ratio":
            prompts.view_weekly_habits_completion_ratio()
        elif choice == "Back":
            break

# Start the program with the interactive menu
if __name__ == "__main__":
    start()