# config/log_config.py
import logging
import colorlog
import sys
from logging.handlers import RotatingFileHandler

class Logger:
    logger = None
    def __new__(cls):
        return None

    @classmethod
    def setup_logging(cls):
        cls.logger = logging.getLogger(__name__)
        if cls.logger.handlers:
            cls.logger.handlers.clear()
        cls.logger.setLevel(logging.DEBUG)

        file_handler = RotatingFileHandler(
            "app.log",
            maxBytes=1024 * 1024,  # 1 MB
            backupCount=10
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
        file_handler.setFormatter(file_formatter)




        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.DEBUG)
        console_handler = colorlog.StreamHandler(stream=sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        # formatter = logging.Formatter('%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s')
        # console_handler.setFormatter(formatter)
        console_formatter = colorlog.ColoredFormatter(
            # '%(log_color)s%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s',
            '%(log_color)s%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d]%(reset)s - %(message)s',
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            reset=True
        )
        console_handler.setFormatter(console_formatter)

        cls.logger.addHandler(file_handler)
        cls.logger.addHandler(console_handler)
        # cls.logger.propagate = False

        # return logger

    @classmethod
    def get_logger(cls):
        return cls.logger

Logger.setup_logging()
logger = Logger.get_logger()
