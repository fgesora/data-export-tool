import os
import time
import logging

from datetime import datetime

import pandas as pd

from colorama import Fore
from tqdm import tqdm

from core.query.fetch_data import DatabaseManager
from settings import export_file_path


class DataExporter:
    def __init__(self):
        self.database_manager = DatabaseManager()

    def export(self, table_name, query, export_format=None, file_name=None, append_data=None, output_path=None):
        start_time = time.monotonic()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        try:
            # Create export directory if it does not exist
            export_path = export_file_path
            os.makedirs(export_path, exist_ok=True)

            # Create file path with file extension
            file_extension = '.' + export_format.lower()
            if file_name is None:
                file_name = f"{table_name}_{timestamp}{file_extension}"
            else:
                file_name += file_extension

            # Combine file path and name
            file_path = os.path.join(export_path, file_name)

            # Check if file exists and handle append option
            if append_data and os.path.isfile(file_path):
                if export_format == 'csv':
                    mode = 'a'
                else:
                    raise ValueError(f"Append option not supported for {export_format} format")
            else:
                mode = 'w'

            if export_format == 'xlsx':
                self._export_to_excel(file_path, table_name, query)
                print(f"\nData exported to {file_path}")
                print("--- %s seconds ---" % (time.monotonic() - start_time))

            elif export_format == 'csv':
                self._export_to_csv(file_path, mode, query)
                print(f"\nData exported to {file_path}")
                print("--- %s seconds ---" % (time.monotonic() - start_time))

            elif export_format == 'json':
                self._export_to_json(file_path, query)
                print(Fore.LIGHTBLUE_EX, f"\nData exported to {file_path}")
                print(Fore.LIGHTBLUE_EX, "--- %s seconds ---" % (time.monotonic() - start_time))

            else:
                # raise an error if export format is not supported
                raise ValueError(f"Unsupported export format: {export_format}")

        except Exception as e:
            # log the error message
            logging.error(f"An error occurred while exporting table data: {e}")

        finally:
            # Log the completion message
            logging.info("Export operation completed.")

    def _export_to_excel(self, file_path, table_name, query):
        # fetch data from the table
        header, rows = self.database_manager.fetch_table_data(query)

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=header)

        # Create a progress bar
        progress_bar = tqdm(total=len(df), desc='Exporting to Excel', unit='row')

        # Write DataFrame to Excel file
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name=table_name, index=False)

        progress_bar.update(len(df))
        progress_bar.close()

    def _export_to_csv(self, file_path, mode, query):
        # fetch data from the table
        header, rows = self.database_manager.fetch_table_data(query)

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=header)

        # Create a progress bar
        progress_bar = tqdm(total=len(df), desc='Exporting to CSV', unit='row')
        # Write DataFrame to CSV file
        with open(file_path, mode, newline='') as csvfile:
            df.to_csv(csvfile, header=(mode == 'w'), index=False, lineterminator='\n', chunksize=1000, encoding='utf-8')

        progress_bar.update(len(df))

        progress_bar.close()

    def _export_to_json(self, file_path, query):
        # fetch data from the table
        header, rows = self.database_manager.fetch_table_data(query)

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=header)

        # Create a progress bar
        progress_bar = tqdm(total=len(df), desc='Exporting to JSON', unit='row')

        # Write DataFrame to JSON file
        with open(file_path, 'w') as jsonfile:
            df.to_json(jsonfile, orient='records', indent=4)

        progress_bar.update(len(df))
        progress_bar.close()
