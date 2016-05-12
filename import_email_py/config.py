from peewee import *

db = MySQLDatabase('rapv_research', user='root', password='1234', charset='utf8', unix_socket='/var/mysql/mysql.sock')