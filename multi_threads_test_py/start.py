import threading

from email_check import EmailCheck
import time


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
