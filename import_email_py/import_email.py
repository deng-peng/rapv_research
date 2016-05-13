import codecs
from peewee import *
from config import db


class People(Model):
    email = CharField()
    working = CharField()
    message = CharField()
    profile_url = CharField()

    class Meta:
        database = db


count = 0
f = codecs.open('email1.txt', 'r', encoding='utf-8')
for line in f.readlines():
    count += 1
    print count
    print line.strip()
    with db.atomic():
        People.create(email=line.strip(), working='', message='', profile_url='')
