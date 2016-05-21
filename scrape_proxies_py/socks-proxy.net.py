from datetime import datetime

import requests
from pyquery import PyQuery as pq
from peewee import *

db = MySQLDatabase('rapv_research', user='root', password='1234', charset='utf8', unix_socket='/var/mysql/mysql.sock')


class Proxies(Model):
    host = CharField()
    port = CharField()
    protocol = CharField()
    created_at = TimeField(default=datetime.today())

    class Meta:
        database = db


def insert_proxy(host, port, protocol):
    if host == '' or port == '' or protocol == '':
        return
    try:
        p = Proxies(ip=host, port=port, protocol=protocol)
        p.save()
    except IntegrityError:
        print 'duplicated'
        pass


if __name__ == '__main__':
    r = requests.get('http://www.socks-proxy.net/')
    d = pq(r.text)
    count = len(d('table tr'))
    if count > 1:
        for i in range(1, count):
            tr = d('table tr').eq(i)
            host = tr('td').eq(0).text().strip()
            port = tr('td').eq(1).text().strip()
            protocol = tr('td').eq(4).text().strip().lower()
            insert_proxy(host, port, protocol)
