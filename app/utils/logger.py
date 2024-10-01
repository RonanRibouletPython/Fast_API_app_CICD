import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

log_file_path = os.getenv('LOG_FILE_PATH')

# ANSI escape codes for colors
COLORS = {
    'reset': '\033[0m',
    'cyan': '\033[36m',
    'yellow': '\033[33m',
    'red': '\033[31m',
    'white': '\033[37m',
}

class CustomFormatter(logging.Formatter):
    """Custom logging formatter with colors for console."""
    
    def format(self, record):
        log_fmt = self._get_colorized_format(record) if hasattr(record, 'funcName') else self._default_format(record)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

    def _get_colorized_format(self, record):
        if record.levelno == logging.DEBUG:
            color = COLORS['cyan']
        elif record.levelno == logging.WARNING:
            color = COLORS['yellow']
        elif record.levelno == logging.ERROR:
            color = COLORS['red']
        else:
            color = COLORS['white']
        
        log_fmt = f"{color}%(asctime)s - %(funcName)s - %(levelname)s - %(message)s{COLORS['reset']}"
        return log_fmt
    
    def _default_format(self, record):
        """Format for the file log (without color)."""
        return "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Console handler (StreamHandler)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = CustomFormatter()
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# File handler (FileHandler or RotatingFileHandler)
file_handler = RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=5)
file_handler.setLevel(logging.INFO)
file_formatter = CustomFormatter()
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)