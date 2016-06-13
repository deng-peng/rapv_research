import requests
from pyquery import PyQuery as pq

s = requests.Session()

# login
r = s.get('https://www.linkedin.com')
html = r.text[r.text.index('<html'):r.text.index('</html>') + 7]
d = pq(html)
csrf = d('input[name=loginCsrfParam]').attr('value')
sa = d('input[name=sourceAlias]').attr('value')
payload = {'session_key': 'xxx@xxx.com', 'session_password': 'xxxxxx', 'isJsEnabled': False,
           'loginCsrfParam': csrf, 'sourceAlias': sa, 'submit': 'Sign in'}
r = s.post('https://www.linkedin.com/uas/login-submit', data=payload)

tasks = [
    'https://www.linkedin.com/profile/view?id=AAoAAAD-xPUBPNWawMXi-tfFWjxa8BmJBnQM6LI&authType=name&authToken=aLSV&trk=api*a109924*s118458*',
    'https://www.linkedin.com/profile/view?id=AAoAAAjvJfEBOCQoj3LTsKCqNkL5TH9kGVjkMQw&authType=name&authToken=dQG8&trk=api*a109924*s118458*'
]


def get_public_url(text):
    target = ';newUrlWithVanity=\'/in/'
    start = text.find(target)
    if start > 0:
        end = text.find('\'', start + len(target))
        return text[start + len(target):end]
    return False


def save_result(p_id, public_url_vanity):
    pass


for url in tasks:
    r = s.get(url)
    public_url_vanity = get_public_url(r.text)
    if public_url_vanity:
        save_result(1, public_url_vanity)
