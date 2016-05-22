import threading
import time
import logging


class EmailCheck(object):
    def __init__(self):
        self.token = 1

    def check(self):
        s = '{0} : {1}'.format(threading.current_thread().name, self.token)
        print s
        logging.info(s)
        self.token += 1
