from __init__ import *
from email_check import EmailCheck

email_checker = EmailCheck()
count = 0
single_count = 0
while True:
    # get token for batch emails
    header_for_batch = email_checker.make_header()
    # limit search for single account
    if single_count >= 1000:
        print 'search {0} emails for this account'.format(single_count)
        email_checker.set_account_status('frozen')
        email_checker.token = ''
        single_count = 0
        continue
    # get tasks for specific account
    r = requests.post(master_url + '/task')
    js = r.json()
    (seq, emails) = js.popitem()
    print emails
    # no more emails
    if len(emails) == 0:
        email_checker.set_account_status('active')
        break

    results = {}
    for address in emails:
        count += 1
        single_count += 1
        res = email_checker.check(address, header_for_batch)
        print res
        if res:
            results[address] = res
        else:
            results[address] = []
        if count % 8 == 0:
            time.sleep(1)
        print 'check count : {0}'.format(count)
    payload = json.dumps(results)
    r = requests.post(master_url + '/result', data={'result': payload})
    print r.text
    if r.text != 'ok':
        email_checker.set_account_status('active')
        break
    else:
        time.sleep(3)
