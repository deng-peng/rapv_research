import codecs
from datetime import *
from email.utils import parseaddr


def parse_email(s):
    s = s.strip().lower()
    arr = s.split('","')
    if len(arr) >= 3:
        em = arr[2]
        if is_email_valid(em):
            return em
    return False


def is_email_valid(s):
    if '%' in s or '@' not in parseaddr(s)[1]:
        return False
    if s.endswith('@') or s.startswith('@'):
        return False
    if s.endswith('.ru') or s.endswith('.fr'):
        return False
    return True


count = 0
success_count = 0
batch = 10000
priority = 1
result = {}
# f = codecs.open('/home/forge/email_list/twitter.txt', 'r', encoding='utf-8')
f = codecs.open('./data/1.csv', 'r', encoding='utf-8')
for line in f:
    count += 1
    if count <= 0:
        continue

    email = parse_email(line)
    if email:
        arr = email.split('@')
        if arr[1] in result:
            result[arr[1]] += 1
        else:
            result[arr[1]] = 1
    if count % batch == 0:
        print '{0} : count : {1}'.format(datetime.now(), count)

result = sorted(result.iteritems(), key=lambda d: d[1], reverse=True)
top = 0
for k, v in result:
    top += 1
    print '{} : {} : {}'.format(top, k, v)
    if top > 199:
        break
