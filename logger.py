import os
import logging
import config
from time import gmtime, strftime


class Logger:

    def __init__(self):
        self.logger = logging.getLogger()

        logfile = config.logger['file_path']
        logfile_location = config.logger['logfile_location']

        if not os.path.exists(logfile):
            os.makedirs(logfile_location, exist_ok=True)

        debug_handler = logging.FileHandler(filename=logfile + '.log')
        debug_handler.setLevel(logging.DEBUG)
        error_handler = logging.FileHandler(filename=logfile + '_ERRORS.log')
        error_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        debug_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        self.logger.addHandler(debug_handler)
        self.logger.addHandler(error_handler)
        self.logger.debug(
            f'LOGFILE CREATED AT: {strftime("%Y-%m-%d %H:%M:%S", gmtime())}')



