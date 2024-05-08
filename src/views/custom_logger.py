import logging
import traceback
import os
from datetime import datetime
from src.config import config


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = "\x1b[1;30m"
    brown = "\x1b[1;35m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    orange = "\x1b[33m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.brown + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%D %H:%M:%S")
        return formatter.format(record)


class CustomLoger:
    def __init__(self, format: str, file_handler: logging.FileHandler = None) -> None:
        self.logger = logging.getLogger(__name__)
        self.format = format

        # Create stdout handler for logging to the console (logs all five levels)
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(CustomFormatter(format))

        # Create file handler for logging to a file (logs all five levels)
        self.file_handler = file_handler
        if self.file_handler is not None:
            self.file_handler.setFormatter(logging.Formatter(format))

        # Create custom logger logging all five levels
        self.set_level(logging.DEBUG)
        self.__init_handlers()

    def __init_handlers(self):
        self.logger.addHandler(self.stream_handler)
        if self.file_handler is not None:
            self.logger.addHandler(self.file_handler)

    def setup_file_handler(self, log_dir: str = "logs", name: str = None):
        if name is None:
            name = ""

        dt_string = datetime.now().strftime("__%Y_%m_%d__%H_%M_%S")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "log_" + name + dt_string + ".log")
        file_handler = logging.FileHandler(log_path)

        self.file_handler = file_handler
        self.file_handler.setFormatter(logging.Formatter(self.format))
        self.logger.addHandler(self.file_handler)

    def set_level(self, level: int):
        self.logger.setLevel(level)
        self.stream_handler.setLevel(level)
        if self.file_handler is not None:
            self.file_handler.setLevel(level)

    def d(self, message: str = "", tag: str = None):
        try:
            if tag is None:
                self.logger.debug(message)
            else:
                self.logger.debug(f"{tag}: {message}")
        except Exception:
            pass

    def i(self, message: str = "", tag: str = None):
        try:
            if tag is None:
                self.logger.info(message)
            else:
                self.logger.info(f"{tag}: {message}")
        except Exception:
            pass

    def w(self, message: str = "", tag: str = None):
        try:
            if tag is None:
                self.logger.warning(message)
            else:
                self.logger.warning(f"{tag}: {message}")
        except Exception:
            pass

    def e(self, message: str = "", tag: str = None, trace_error: bool = True):
        try:
            if tag is None:
                self.logger.error(message)
            else:
                self.logger.error(f"{tag}: {message}")

            if trace_error:
                self.logger.error(traceback.format_exc())
        except Exception:
            pass

    def c(self, message: str = "", tag: str = None):
        try:
            if tag is None:
                self.logger.debug(message)
            else:
                self.logger.debug(f"{tag}: {message}")
        except Exception:
            pass


# dt_string = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
# logs_dir = "logs"
# os.makedirs(logs_dir, exist_ok=True)
# log_path = os.path.join(logs_dir, "log__" + dt_string + ".log")
# file_handler = logging.FileHandler(log_path)

logger = CustomLoger(format=f"[{config.get('name', '')}][%(asctime)s][%(levelname).1s] %(message)s", file_handler=None)
