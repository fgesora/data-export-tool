import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from main import Main


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.main = Main()

    @patch("builtins.input", side_effect=["1", "n"])
    @patch("builtins.print")
    def test_run_with_preset_queries(self, mock_print, mock_input):
        self.main.handle_preset_queries = MagicMock()
        self.main.run()
        self.main.handle_preset_queries.assert_called_once()

    @patch("builtins.input", side_effect=["2", "n"])
    @patch("builtins.print")
    def test_run_with_custom_query(self, mock_print, mock_input):
        self.main.handle_custom_query = MagicMock()
        self.main.run()
        self.main.handle_custom_query.assert_called_once()

    @patch("builtins.input", side_effect=["3"])
    @patch("builtins.print")
    @patch("builtins.exit")
    def test_run_with_query_update(self, mock_exit, mock_print, mock_input):
        self.main.handle_query_update = MagicMock()
        self.main.run()
        self.main.handle_query_update.assert_called_once()
        mock_exit.assert_called_once()

    @patch("builtins.input", side_effect=["invalid", "n"])
    @patch("builtins.print")
    def test_run_with_invalid_choice(self, mock_print, mock_input):
        self.main.run()
        mock_print.assert_called_with("\x1b[91mInvalid choice. Please enter 1, 2, or 3.")

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    @patch("builtins.print")
    def test_run_with_keyboard_interrupt(self, mock_print, mock_input):
        self.main.run()
        mock_print.assert_called_with("\x1b[91mExport canceled by user.")

    @patch("builtins.input", side_effect=ValueError)
    @patch("builtins.print")
    def test_run_with_value_error(self, mock_print, mock_input):
        self.main.run()
        mock_print.assert_called_with("\x1b[91mInvalid input. Please enter a valid number.")

    @patch("logging.error")
    @patch("builtins.input", side_effect=["1", "n"])
    @patch("builtins.print")
    def test_run_with_export_error(self, mock_print, mock_input, mock_logging_error):
        self.main.export_engine.export_table_data = MagicMock(side_effect=Exception("Export error"))
        self.main.run()
        mock_logging_error.assert_called_once_with("An error occurred while exporting table data: Export error")
        mock_print.assert_called_with("\x1b[91mAn error occurred while exporting table data: Export error")

    @patch("builtins.input", side_effect=["1", "y", "n"])
    @patch("builtins.print")
    def test_run_multiple_exports(self, mock_print, mock_input):
        self.main.handle_preset_queries = MagicMock()
        self.main.run()
        self.assertEqual(self.main.handle_preset_queries.call_count, 2)

    def test_handle_custom_query(self):
        self.main.query_prompter.get_custom_query = MagicMock(return_value=("table1", "query1"))
        self.main.handle_export = MagicMock()

        self.main.handle_custom_query()

        self.main.query_prompter.get_custom_query.assert_called_once_with(self.main.query_manager)
        self.main.handle_export.assert_called_once_with([("table1", "query1")])

    def test_handle_query_update(self):
        self.main.query_manager.retrieve_preset_queries = MagicMock()
        self.main.query_prompter.update_query = MagicMock()

        self.main.handle_query_update()

        self.main.query_manager.retrieve_preset_queries.assert_called_once()
        self.main.query_prompter.update_query.assert_called_once_with(self.main.query_manager)

    @patch("builtins.input", side_effect=["csv", "output.csv"])
    def test_handle_export(self, mock_input):
        self.main.export_manager.get_export_format_choice = MagicMock(return_value="csv")
        self.main.export_manager.get_output_path = MagicMock(return_value="output.csv")
        self.main.export_engine.export_table_data = MagicMock()

        queries = [("table1", "query1"), ("table2", "query2")]

        self.main.handle_export(queries)

        self.main.export_manager.get_export_format_choice.assert_called_once()
        self.main.export_manager.get_output_path.assert_called_once()
        self.main.export_engine.export_table_data.assert_called_with("table1", "query1", "csv", "output.csv")


if __name__ == "__main__":
    unittest.main()


