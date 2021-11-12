#!/usr/env bin python3
import logging
from datetime import datetime
import os

FORMAT_LOG = "%(asctime)s|%(levelname)s|%(message)s"

class ControllerLogger(object):
    def __init__(self):
        self.path_log_application = os.path.join(os.getcwd(), "logs/logs_aci_{}.log".format(datetime.now().strftime("%Y%m")))

    def config_upload(self):
        logging.basicConfig(filename=self.path_log_application, format=FORMAT_LOG,
                            filemode='a', level=logging.DEBUG)

    def set_log_app(self, type_log, message):
        self.config_upload()
        if type_log.lower() == 'info':
            logging.info(message)
        elif type_log.lower() == 'warning':
            logging.warning(message)
        elif type_log.lower() == 'critical':
            logging.critical(message)
        else:
            return None