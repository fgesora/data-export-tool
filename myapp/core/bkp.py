import os
import logging
import customtkinter as ctk
from typing import List
from tkinter import Tk, messagebox
from tkinter.filedialog import askdirectory
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from colorama import Fore
from core.query.db_functions import QueryManager
from core.export import ExportEngine


class CustomTkinterGUI:
    def __init__(self, title, geometry="500x400"):
        self.root = ctk.CTk()
        self.root.title(title)
        self.root.geometry(geometry)
        self.frame = ctk.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.widgets = []

    def add_label(self, text, font=("Roboto", 24), **kwargs):
        label = ctk.CTkLabel(master=self.frame, text=text, font=font, **kwargs)
        label.pack(pady=12, padx=10)
        self.widgets.append(label)

    def add_entry(self, placeholder_text, font=("Roboto", 12), show="", **kwargs):
        entry = ctk.CTkEntry(master=self.frame, placeholder_text=placeholder_text, font=font, show=show, **kwargs)
        entry.pack(pady=12, padx=10)
        self.widgets.append(entry)
        return entry

    def add_button(self, text, command=None, **kwargs):
        button = ctk.CTkButton(master=self.frame, text=text, command=command)
        button.pack(pady=12, padx=10)
        self.widgets.append(button)
        return button

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def run(self):
        self.root.mainloop()


class QueryPrompter:
    @staticmethod
    def update_query(query_manager: QueryManager) -> None:
        """
        Update a query in the database.
        """
        print("\n" + Fore.BLUE + "Available queries:")
        try:
            queries = query_manager.retrieve_preset_queries()
            print(Fore.BLUE + "Please select a preset query:")
            QueryPrompter.print_query_list(queries)
            choice = QueryPrompter.prompt_for_query_choice(queries)
            if choice is None:
                return
            query_index = choice - 1
            selected_query = queries[query_index]
            new_query = QueryPrompter.prompt_for_new_query(selected_query[0])
            if new_query is None:
                return
            QueryPrompter.update_query_in_list(queries, query_index, new_query)
            query_manager.update_query_in_database(selected_query[0], new_query)
        except Exception as e:
            logging.error("Failed to update query: %s", e)

    @staticmethod
    def prompt_for_query_choice(queries):
        """
        Prompt the user to select a query from the list.

        Args:
            queries (list): A list of query tuples containing table names and query texts.

        Returns:
            int: The index of the selected query, or None if no query was selected.
        """
        completer = WordCompleter([str(i) for i in range(1, len(queries) + 1)])
        choice = prompt(
            Fore.CYAN + "Enter the number of the query to update (or 'q' to cancel): ",
            completer=completer,
        )
        if choice.lower() == "q":
            return None
        return int(choice)

    @staticmethod
    def get_query_choices(queries: List[str]) -> List[str]:
        """
        Prompt the user to select multiple queries from the list.

        Args:
            queries (List[str]): A list of queries.

        Returns:
            List[str]: The selected queries.
        """
        print(Fore.CYAN + "Enter the numbers of the queries to run (separated by commas):")
        QueryPrompter.print_query_list(queries)
        choices = prompt("> ").split(",")
        return [queries[int(choice) - 1] for choice in choices]

    @staticmethod
    def prompt_for_new_query(query_name):
        """
        Prompt the user to enter a new query.

        Args:
            query_name (str): The name of the query to be updated.

        Returns:
            str: The new query text, or None if no query was entered.
        """
        print(Fore.CYAN + f"Enter the new query for {query_name} (or 'q' to cancel):")
        new_query = prompt("> ")
        if new_query.lower() == "q":
            return None
        return new_query

    @staticmethod
    def get_custom_query(query_manager: QueryManager) -> tuple:
        """
        Prompt the user to enter a custom query.
        """
        table_name = input(Fore.BLUE + "Enter the name of the table to export: ")
        query = input("Enter the SQL query to export the table: ")

        save_query = input(Fore.BLUE + "Do you want to save this custom query for future use? [y/n]: ")
        if save_query.lower() == "y":
            # Save the query to the database
            query_manager.save_query_to_db(table_name, query)
            print(Fore.GREEN + "Custom query saved successfully!")

        return table_name, query

    @staticmethod
    def update_query_in_list(queries: list, query_index: int, new_query: str) -> None:
        """
        Update a query in the list of queries.

        Args:
            queries (list): A list of query tuples containing table names and query texts.
            query_index (int): The index of the query to be updated.
            new_query (str): The new query text.
        """
        table_name, _ = queries[query_index]
        queries[query_index] = (table_name, new_query)
        print(Fore.GREEN + "Query updated successfully!")

    @staticmethod
    def print_query_list(queries: list) -> None:
        """
        Print a list of available queries.

        Args:
            queries (list): A list of query tuples containing table names and query texts.
        """
        for i, (table_name, _) in enumerate(queries, start=1):
            print(Fore.CYAN + f"{i}. {table_name}")

    @staticmethod
    def get_preset_query_choice(queries: list) -> None:
        """
        Prompt the user to choose a preset query.
        """
        print(Fore.BLUE + "Please select a preset query:")
        for i, (table_name, query) in enumerate(queries, start=1):
            print(Fore.CYAN + f"{i}. {table_name}")

        while True:
            try:
                choice = int(input("Enter your choice: "))
                if 1 <= choice <= len(queries):
                    return queries[choice - 1]
                print(Fore.LIGHTRED_EX + "Invalid choice. Please enter a valid number.")
            except ValueError:
                print(Fore.LIGHTRED_EX + "Invalid input. Please enter a number.")


class ExportManager:
    @staticmethod
    def print_export_formats():
        """
        Print the available export file formats.
        """
        print(Fore.LIGHTBLUE_EX + "--------------FILE EXPORT--------------")
        print(Fore.BLUE + "Please select an export file format:")
        print(Fore.CYAN + "1. CSV")
        print(Fore.LIGHTGREEN_EX + "2. XLSX")
        print(Fore.MAGENTA + "3. JSON")
        print(Fore.LIGHTBLUE_EX + "---------------------------------------")

    @staticmethod
    def get_export_format_choice():
        """
        Prompt the user to choose the export format.
        """
        ExportManager.print_export_formats()
        choice = ""
        while choice not in ["1", "2", "3"]:
            choice = input("Enter your choice: ")
        export_format = {"1": "csv", "2": "xlsx", "3": "json"}[choice]
        return export_format

    @staticmethod
    def get_output_path():
        """
        Prompt the user to enter the output file path.
        """
        Tk().withdraw()
        output_path = askdirectory(title="Select a folder to save the file")
        if not output_path:
            print(Fore.RED + "Export canceled.")
            exit()
        else:
            # Check if the output directory exists, create it if it doesn't
            os.makedirs(output_path, exist_ok=True)
        return output_path


class MainApplication:
    def __init__(self):
        self.query_manager = QueryManager()
        self.query_prompter = QueryPrompter()
        self.export_manager = ExportManager()
        self.export_engine = ExportEngine()
        self.gui = CustomTkinterGUI("Data Export")

        # Add GUI elements
        # Add GUI elements
        self.gui.add_label("Database Export", font=("Roboto", 24))
        self.gui.add_label("Select Export Options:", font=("Roboto", 16))
        self.gui.add_button("Export Data", command=self.get_and_save_queries)

    def get_and_save_queries(self):
        """
        Get user input for query selection and export options.
        """
        try:
            choice = input(
                Fore.BLUE + "Do you want to use preset queries, enter your own, or update an existing query? "
                            "[1 for preset, 2 for custom, 3 for update]: "
            )

            if choice == "1":
                queries = self.query_manager.retrieve_preset_queries()
                selected_queries = self.query_prompter.get_query_choices(queries)
            elif choice == "2":
                selected_queries = [self.query_prompter.get_custom_query(self.query_manager)]
            elif choice == "3":
                self.query_manager.retrieve_preset_queries()
                self.query_prompter.update_query(self.query_manager)
                exit()
            else:
                print(Fore.LIGHTRED_EX + "Invalid choice. Please enter 1, 2, or 3.")
                return

            export_format = self.export_manager.get_export_format_choice()
            output_path = self.export_manager.get_output_path()

            for table_name, query in selected_queries:
                self.export_engine.export_table_data(table_name, query, export_format, output_path)
        except KeyboardInterrupt:
            print(Fore.LIGHTRED_EX + "Export canceled by the user.")
        except ValueError:
            print(Fore.LIGHTRED_EX + "Invalid input. Please enter a valid number.")
        except Exception as e:
            logging.error(f"An error occurred while exporting table data: {e}")
            print(Fore.LIGHTRED_EX + f"An error occurred while exporting table data: {e}")
