class ExportPrompter:
    @staticmethod
    def prompt_export_time():
        """Prompt the user to enter the export time in HH:MM format."""
        while True:
            export_time = input("Enter the export time (in HH:MM format): ")
            if len(export_time) == 5 and export_time.count(":") == 1:
                hour, minute = export_time.split(":")
                if hour.isdigit() and minute.isdigit() and 0 <= int(hour) < 24 and 0 <= int(minute) < 60:
                    return export_time
            print("Invalid export time format. Please enter a valid time in HH:MM format.")

    @staticmethod
    def prompt_export_times():
        """Prompt the user to enter multiple export times in HH:MM format."""
        export_times = []
        while True:
            export_time = ExportPrompter.prompt_export_time()
            export_times.append(export_time)
            add_another = input("Do you want to add another export time? (y/n): ")
            if add_another.lower() != "y":
                break
        return export_times

    @staticmethod
    def prompt_table_selection(tables_and_queries):
        """Prompt the user to select the tables/queries to export."""
        print("Available Tables/Queries:")
        for index, (table_name, _) in enumerate(tables_and_queries, start=1):
            print(f"{index}. {table_name}")

        while True:
            selection = input("Enter the numbers of the tables/queries to export (separated by commas): ")
            selected_indices = [int(i) - 1 for i in selection.split(",")]
            if all(0 <= index < len(tables_and_queries) for index in selected_indices):
                return [tables_and_queries[i] for i in selected_indices]
            print("Invalid selection. Please enter valid numbers of the tables/queries.")

    @staticmethod
    def prompt_export_format(available_formats):
        """Prompt the user to select the export format."""
        print("Available Export Formats:")
        for index, export_format in enumerate(available_formats, start=1):
            print(f"{index}. {export_format}")

        while True:
            format_selection = input("Enter the number of the export format: ")
            if format_selection.isdigit() and 1 <= int(format_selection) <= len(available_formats):
                return available_formats[int(format_selection) - 1]
            print("Invalid format selection. Please enter a valid number.")
