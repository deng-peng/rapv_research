import requests

proxies = {
    "https": "socks5://127.0.1.1:1080",
}
try:
    r = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=30)
    print r.text
except requests.exceptions.ConnectTimeout, e:
    print 't'
    print e
except requests.exceptions.ConnectionError, e:
    print 'c'
    print e
except Exception, e:
    print 'e'
    print e
