import requests
import time

# url = 'https://api.linkedin.com/v1/people/email=rob%40dealsextra.com.au:(first-name,last-name,headline,location,distance,positions,twitter-accounts,im-accounts,phone-numbers,member-url-resources,picture-urls::(original),site-standard-profile-request,public-profile-url,relation-to-viewer:(connections:(person:(first-name,last-name,headline,site-standard-profile-request,picture-urls::(original)))))'
url = 'https://api.linkedin.com/v1/people/email={}:(first-name,last-name,headline,location,distance,positions,twitter-accounts,im-accounts,phone-numbers,member-url-resources,picture-urls::(original),site-standard-profile-request,public-profile-url,relation-to-viewer:(connections:(person:(first-name,last-name,headline,site-standard-profile-request,picture-urls::(original)))))'
headers = {'x-requested-with': 'IN.XDCall',
           'x-li-format': 'json',
           'x-http-method-override': 'GET',
           'x-cross-domain-origin': 'https://mail.google.com',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
           'oauth_token': '58hWTzXKK9iaL9wReP7RP4ZPYOjbdgKv8BH2',
           'content-type': 'application/json'
           }
# 15:15
email_list = [
    'donella.davidson@citi.com',
    'maria_campos@live.com.au',
    'mthom@doh.health.nsw.gov.au',
    'lozleo@hotmail.com',
]
count = 1
for email in email_list:
    print(count)
    count += 1
    try:
        r = requests.get(url.format(email.replace('@', '%40')), headers=headers, timeout=30)
        js = r.json()
        print js
        if 'errorCode' in js:
            print '{0} : {1}'.format(email, js['status'])
        elif 'publicProfileUrl' in js:
            print '{0} : {1}'.format(email, js['publicProfileUrl'])
    except Exception, e:
        print(e)
        print(email)
