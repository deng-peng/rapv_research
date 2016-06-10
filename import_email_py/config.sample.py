import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='rapv_research',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
