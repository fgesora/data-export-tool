import logging
import schedule
import time

from core.query.db_functions import QueryManager
from core.export.engine import DataExporter
from scheduler.interface.schedule_user_interface import ExportPrompter


class ExportScheduler:
    def __init__(self):
        self.query_manager = QueryManager()
        self.data_exporter = DataExporter()
        self.export_prompter = ExportPrompter()
        self.tables_and_queries = []
        self.export_times = []
        self.selected_tables_and_queries = []
        self.export_format = ""

    def schedule_exports(self):
        for export_time in self.export_times:
            for table_name, query in self.selected_tables_and_queries:
                try:
                    # Schedule the export task for the current time and format
                    schedule.every().day.at(export_time).do(
                        self.export_table_data, table_name, query, self.export_format
                    )
                    logging.info(f"Export scheduled for {table_name} at {export_time}")
                    print(f"Export scheduled for {table_name} at {export_time}")
                except ValueError as ve:
                    logging.error(f"Failed to schedule export for {table_name}: {str(ve)}")
                    print(f"Failed to schedule export for {table_name}: {str(ve)}")

    def export_table_data(self, table_name, query, export_format):
        try:
            # Export the data using the selected options
            self.data_exporter.export(table_name, query, export_format)
            logging.info("Data exported successfully!")
        except Exception as e:
            logging.error(f"An error occurred while exporting table data: {e}")

    def run(self):
        try:
            # Fetch available tables and queries from the database
            self.tables_and_queries = self.query_manager.retrieve_preset_queries()

            # Prompt the user for export times
            self.export_times = self.export_prompter.prompt_export_times()

            # Prompt the user to select tables/queries to export
            self.selected_tables_and_queries = self.export_prompter.prompt_table_selection(self.tables_and_queries)

            # Prompt the user for export format
            available_formats = ["csv", "xlsx", "json"]
            self.export_format = self.export_prompter.prompt_export_format(available_formats)

            # Schedule the exports at the specified times
            self.schedule_exports()

            # Run the schedule tasks
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Export script stopped by user.")
