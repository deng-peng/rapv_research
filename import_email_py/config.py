import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='rapv_research',
                             charset='utf8',
                             unix_socket='/var/mysql/mysql.sock',
                             cursorclass=pymysql.cursors.DictCursor)


# db = MySQLDatabase('rapv_research', user='root', password='1234', charset='utf8', unix_socket='/var/mysql/mysql.sock')
