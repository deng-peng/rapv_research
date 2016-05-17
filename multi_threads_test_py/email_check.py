import threading


class EmailCheck(object):
    def __init__(self):
        self.token = 1

    def check(self):
        print '{0} : {1}'.format(threading.current_thread().name, self.token)
        self.token += 1
