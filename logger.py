import errno
import os
import logging
import sys
import config
from time import gmtime, strftime


class Logger:

    def __init__(self, args):
        self.logger = logging.getLogger()
        self.args = args
        if self.args['debug']:
            self.logger.setLevel(logging.DEBUG)
        logfile = config.logger['file_path']
        logfile_location = config.logger['logfile_location']

        if not os.path.exists(logfile):
            os.makedirs(logfile_location, exist_ok=True)
            logging.basicConfig(filename=logfile, level=logging.DEBUG, filemode='w')
        file_handler = logging.FileHandler(logfile)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        self.logger.addHandler(file_handler)
        self.logger.debug(
            f'LOGFILE CREATED AT: {strftime("%Y-%m-%d %H:%M:%S", gmtime())}')


