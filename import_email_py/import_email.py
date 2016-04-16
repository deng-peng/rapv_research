import codecs

from peewee import *

db = MySQLDatabase('rapv_research', user='root', password='1234', charset='utf8', unix_socket='/var/mysql/mysql.sock')


class People(Model):
    email = CharField()
    working = CharField()
    message = CharField()
    profile_url = CharField()

    class Meta:
        database = db


count = 0
f = codecs.open('email.txt', 'r', encoding='utf-8')
for line in f.readlines():
    count += 1
    print count
    p = People(email=line, working='', message='', profile_url='')
    p.save()
