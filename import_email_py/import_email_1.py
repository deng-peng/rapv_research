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
f = codecs.open('email.txt', 'r', encoding='utf-8')
for line in f.readlines():
    count += 1
    print count
    arr = line.split(':')
    if len(arr) > 1:
        try:
            with db.atomic():
                People.create(email=arr[0].strip(), working='', message='', profile_url='')
        except IntegrityError, e:
            print e
