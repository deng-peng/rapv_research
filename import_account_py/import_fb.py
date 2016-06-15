import codecs
import pymysql
from datetime import *

from config import connection


def parse_line(s):
    s = s.strip()
    arr = s.split(':')
    if len(arr) >= 2:
        return arr[0], arr[1]
    return False


f = codecs.open('./data/fb.txt', 'r', encoding='utf-8')
with connection.cursor() as cursor:
    for line in f:
        email, psw = parse_line(line)
        if email:
            table_name = 'accounts'
            sql = "INSERT INTO `{0}` VALUE (NULL, '{1}', '{2}', '0', 'facebook', '', '0', '{3}', '{3}')".format(
                table_name, email, psw, datetime.now())
            try:
                cursor.execute(sql)
            except pymysql.err.IntegrityError:
                pass
            except pymysql.err.ProgrammingError:
                pass
connection.commit()
connection.close()
