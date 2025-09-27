import os
import logging
from time import localtime, strftime

class logger:
    def __init__(self, name='IBbot', use_logging=True):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.use_logging = use_logging

        self.path = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        # Create file handler
        log_file = f"logs/{strftime('%Y-%m-%d_%H-%M-%S', localtime())}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get(self, caller:str) -> logging.Logger:
        """
        Returns the logger instance for the specified caller.
        :param caller: The name of the caller (e.g., module or class name).
        :return: Logger instance.
        """
        if self.use_logging:
            return logging.getLogger(f"{self.logger.name}.{caller}")
        else:
            return logging.getLogger('')
        
    def log(self, message: str):
        """
        Logs a message at the INFO level.
        :param message: The message to log.
        """
        time=strftime('%Y-%m-%d %H:%M:%S', localtime())
        if self.use_logging:
            self.logger.info(message, extra={'time': time})
        else:
            print(f"{time} | {message}")