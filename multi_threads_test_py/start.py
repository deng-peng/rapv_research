import threading
from email_check import EmailCheck
import time

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %X',
                    filename='./logs/log-{0}.txt'.format(time.strftime('%Y-%m-%d', time.localtime())))


def run_thread(number):
    email_checker = EmailCheck()
    email_checker.token = number * 100
    while True:
        email_checker.check()
        time.sleep(2)


if __name__ == '__main__':
    for i in range(3):
        th = threading.Thread(target=run_thread, args=(i,))
        th.start()
