import pymysql.cursors

print('init pymysql')


def getMysqlConnect():
    return pymysql.Connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="mysqlmima123",
        db="huya_download",
        charset='utf8'
    )
