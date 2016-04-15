from __init__ import *
from slave_py.email_check import EmailCheck

email_checker = EmailCheck()

r = requests.get(master_url + '/task')
js = r.json()
(seq, emails) = js.popitem()
print seq
print emails
header_for_batch = email_checker.make_header()
results = {}
for address in emails:
    res = email_checker.check(address, header_for_batch)
    print res
    if res:
        results[address] = res
    else:
        results[address] = ''

payload = json.dumps(results)
r = requests.post(master_url + '/result', data={'result': payload})
print r.text
