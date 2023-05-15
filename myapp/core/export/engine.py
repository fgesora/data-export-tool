import logging

from colorama import Fore

from core.export.export_data import DataExporter


class ExportEngine:
    def __init__(self):
        self.data_exporter = DataExporter()

    def export_table_data(self, table_name, query, export_format, output_path) -> None:
        """
        Export the data using the selected options.
        """
        try:
            self.data_exporter.export(table_name, query, export_format=export_format, output_path=output_path)
            logging.info("Data exported successfully!")
        except Exception as e:
            logging.error(f"An error occurred while exporting table data: {e}")
            print(Fore.LIGHTRED_EX, "Please check the following:")
            print(Fore.LIGHTRED_EX, "- Make sure the table name is spelled correctly.")
            print(Fore.LIGHTRED_EX, "- Make sure the SQL query is valid.")
            print(Fore.LIGHTRED_EX, "- Make sure the output path is a valid directory.")
