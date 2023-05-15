import logging
import sys
import time

from prompt_toolkit.styles import Style
from colorama import Fore

from core.query.db_functions import QueryManager
from core.query.prompter import QueryPrompter
from core.export.manager import ExportManager
from core.export.engine import ExportEngine

# Define the syntax highlighting style
style = Style.from_dict({
    "prompt": "ansicyan",
    "input": "ansiblue",
    "output": "ansigreen",
    "error": "ansired",
    # Add more styles as needed
})


def print_typing(statement):
    for char in statement:
        print(char, end='', flush=True)
        time.sleep(0.5)


def print_loading_progress():
    width = 50
    total_steps = 100
    delay = 0.05

    for step in range(total_steps + 1):
        progress = int((step / total_steps) * width)
        bar = '[' + '=' * progress + ' ' * (width - progress) + ']'
        percentage = f'{step}%'

        sys.stdout.write('\r')
        sys.stdout.write(f'Connecting... {bar} {percentage}')
        sys.stdout.flush()

        time.sleep(delay)


class Main:
    def __init__(self):
        self.query_manager = QueryManager()
        self.query_prompter = QueryPrompter()
        self.export_manager = ExportManager()
        self.export_engine = ExportEngine()

    def run(self) -> None:
        """
        Main function to start the program.
        """
        print(Fore.BLUE + "-------------------WELCOME TO THE DATA EXPORT TOOL!-------------------\n")

        if not self.query_manager.credentials_exist():
            print(Fore.LIGHTRED_EX + "No database credentials found. Please set up the credentials.")
            self.query_manager.setup_database_credentials()

        print_loading_progress()
        print(Fore.GREEN + "\nDatabase connection successful!")

        while True:
            try:
                choice = input(
                    Fore.BLUE +
                    """
            +------------------ DATA EXPORT MENU ------------------+
            |                                                      |
            |            1. Use preset queries                     |
            |            2. Enter and save your own query          |
            |            3. Update an existing query               |
            |                                                      |
            +------------------------------------------------------+
            What would you like to do? """
                )

                if choice == "1":
                    self.handle_preset_queries()
                elif choice == "2":
                    self.handle_custom_query()
                elif choice == "3":
                    self.handle_query_update()
                    exit()
                else:
                    print(Fore.LIGHTRED_EX + "Invalid choice. Please enter 1, 2, or 3.")
                    continue

                continue_choice = input(Fore.BLUE + "Do you want to export another query? [y/n]: ")
                if continue_choice.lower() != "y":
                    break

            except KeyboardInterrupt:
                print(Fore.LIGHTRED_EX, "Export canceled by user.")
                break
            except ValueError:
                print(Fore.LIGHTRED_EX + "Invalid input. Please enter a valid number.")
            except Exception as e:
                logging.error(f"An error occurred while exporting table data: {e}")
                print(Fore.LIGHTRED_EX + f"An error occurred while exporting table data: {e}")

    def handle_preset_queries(self) -> None:
        queries = self.query_manager.retrieve_preset_queries()
        selected_queries = self.query_prompter.get_query_choices(queries)
        self.handle_export(selected_queries)

    def handle_custom_query(self) -> None:
        selected_queries = [self.query_prompter.get_custom_query(self.query_manager)]
        self.handle_export(selected_queries)

    def handle_query_update(self) -> None:
        self.query_manager.retrieve_preset_queries()
        self.query_prompter.update_query(self.query_manager)

    def handle_export(self, queries) -> None:
        """

        :type queries: iter
        """
        export_format = self.export_manager.get_export_format_choice()
        output_path = self.export_manager.get_output_path()

        for table_name, query in queries:
            self.export_engine.export_table_data(table_name, query, export_format, output_path)


if __name__ == "__main__":
    main = Main()
    main.run()
