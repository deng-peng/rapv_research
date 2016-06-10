import codecs
import pymysql
from datetime import *

from config import connection


def parse_email(s):
    s = s.strip().lower()
    arr = s.split(':')
    if len(arr) >= 2:
        return arr[1]
    return False


def get_table_name(m):
    first = m[:1]
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']
    if first in alphabet:
        return 'people_' + first
    return 'people_0'


count = 0
batch = 100
f = codecs.open('./data/linked1.cfg', 'r', encoding='utf-8')
with connection.cursor() as cursor:
    for line in f.readlines():
        count += 1
        email = parse_email(line)
        if email:
            table_name = get_table_name(email)
            sql = "INSERT INTO `{0}` VALUE (0, '{1}','', 0, '', '' ,0, 10)".format(table_name, email)
            try:
                cursor.execute(sql)
            except pymysql.err.IntegrityError:
                print 'duplicate , skip'
        if count % batch == 0:
            connection.commit()
            print '{0} commit success , count : {1}'.format(datetime.now(), count)
            connection.begin()
connection.commit()
connection.close()
