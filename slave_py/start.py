from __init__ import *
from email_check import EmailCheck


def worker():
    email_checker = EmailCheck()
    count = 0
    current_account_count = 0
    while True:
        # get token for batch emails
        header_for_batch = email_checker.make_header()
        # limit search for single account
        if current_account_count >= 1000:
            print 'search {0} emails for this account'.format(current_account_count)
            email_checker.set_account_status('frozen')
            email_checker.token = ''
            current_account_count = 0
            continue
        # get tasks for specific account
        r = requests.post(master_url + '/task')
        js = r.json()
        (seq, emails) = js.popitem()
        # print emails
        # no more emails
        if len(emails) == 0:
            email_checker.set_account_status('active')
            break

        results = {}
        for address in emails:
            count += 1
            current_account_count += 1
            res = email_checker.check(address, header_for_batch)
            print res
            if res:
                results[address] = res
            else:
                results[address] = []
            print '{0} check count : {0}'.format(threading.currentThread().name, count)
        payload = json.dumps(results)
        r = requests.post(master_url + '/result', data={'result': payload})
        print '{0} : {1}'.format(threading.currentThread().name, r.text)
        if r.text != 'ok':
            email_checker.set_account_status('active')
            break


if __name__ == '__main__':
    for i in range(max_threads):
        th = threading.Thread(target=worker)
        th.start()
