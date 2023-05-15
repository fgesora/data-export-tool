import logging
import sys

# Define color codes for different log levels
LOG_COLORS = {
    logging.DEBUG: "\033[1;34m",  # blue
    logging.INFO: "\033[1;32m",  # green
    logging.WARNING: "\033[1;33m",  # yellow
    logging.ERROR: "\033[1;31m",  # red
    logging.CRITICAL: "\033[1;41m",  # white on red background
}


# Define a custom log formatter that includes color codes
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        level_color = LOG_COLORS.get(record.levelno, "")
        reset_color = "\033[0m"
        formatted_message = super().format(record)
        return f"{level_color}{formatted_message}{reset_color}"


def setup_logger(log_file_path):
    # Set up logging with a rotating file handler
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    handler = logging.FileHandler(log_file_path)
    handler.setLevel(logging.DEBUG)

    # Create a console handler with colored output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(ColoredFormatter())

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s [line:%(lineno)d]')

    # Set the format for the file handler
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(handler)
    logger.addHandler(console_handler)
