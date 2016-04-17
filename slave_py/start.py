from __init__ import *
from slave_py.email_check import EmailCheck

email_checker = EmailCheck()
count = 0
while True:
    r = requests.get(master_url + '/task')
    js = r.json()
    (seq, emails) = js.popitem()
    print seq
    print emails
    # no more emails
    if len(emails) == 0:
        email_checker.set_account_status('active')
        break
    # get token for batch emails
    header_for_batch = email_checker.make_header()
    results = {}
    for address in emails:
        res = email_checker.check(address, header_for_batch)
        print res
        if res:
            results[address] = res
        else:
            results[address] = []
        count += 1
        print 'check count : {0}'.format(count)
    payload = json.dumps(results)
    r = requests.post(master_url + '/result', data={'result': payload})
    print r.text
    if r.text != 'ok':
        email_checker.set_account_status('active')
        break
    else:
        time.sleep(3)
