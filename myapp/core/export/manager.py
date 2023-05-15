import os

from tkinter import Tk
from tkinter.filedialog import askdirectory

from colorama import Fore


class ExportManager:
    @staticmethod
    def print_export_formats():
        """
        Print the available export file formats.
        """
        print(
            Fore.LIGHTBLUE_EX +
            """
            +------------------- FILE EXPORT ------------------+
            |                                                  |
            |          Available export file formats:          |
            |                      1. CSV                      |
            |                      2. XLSX                     |
            |                      3. JSON                     |
            |                                                  |
            +--------------------------------------------------+
            Please select an export file format: """
        )

    @staticmethod
    def get_export_format_choice():
        """
        Prompt the user to choose the export format.
        """
        ExportManager.print_export_formats()
        query_choice = ""
        while query_choice not in ["1", "2", "3"]:
            query_choice = input("Enter your query_choice: ")
        export_format = {"1": "csv", "2": "xlsx", "3": "json"}[query_choice]
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
