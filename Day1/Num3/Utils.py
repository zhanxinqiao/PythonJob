
#date:2019/9/20

import  pymysql
import  hashlib

class SqlUtils:
    @staticmethod
    def getConn():
        # 获取连接
        conn = pymysql.connect(host='localhost',user='root',password='123456',database='test')
        return  conn

    @staticmethod
    def close(cursor,conn):
        cursor.close()
        conn.close()

class MD5Utils:
    @staticmethod
    def getMD5(string):
        md5 = hashlib.md5(bytes('salt',encoding='utf-8'))
        md5.update(bytes(string))
        return  md5.hexdigest()
