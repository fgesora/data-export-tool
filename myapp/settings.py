from pathlib import Path

# Get the path of the current script file
script_path = Path(__file__).resolve()

# Get the project directory path
project_dir = script_path.parent.parent

# Define the relative paths
export_dir = project_dir / "exports"
error_log_file = project_dir / "logs" / "error.log"

# Convert paths to optimized string representation
export_file_path = str(export_dir)
error_log_file_path = str(error_log_file)
