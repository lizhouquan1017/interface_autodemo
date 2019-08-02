# coding:utf-8

import pymysql
from database.readPurchase import ReadPurchase

# yaml.warnings({'YAMLLoadWarning': False})
# with open('../config/db.yaml', 'r', encoding='gbk') as file:
#     data = yaml.load(file)

localhost = '10.10.13.120'
username = 'jxc'
password = 'jxc'
database = 'jxc'


class Database(object):

    def __init__(self):
        self._localhost = localhost
        self._username = username
        self._password = password
        self._database = database
        self._conn = self.connmysql()
        if(self._conn):
            self._cursor = self._conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 连接数据库
    def connmysql(self):
        conn = False
        try:
            conn = pymysql.connect(host=self._localhost,user=self._username,password=self._password,database=self._database)
        except Exception:
            conn = False
        return conn

    # 获取查询结果
    def fetch_all(self, sql):
        res = ''
        if(self._conn):
            try:
                self._cursor.execute(sql)
                res =  self._cursor.fetchall()
            except Exception:
                res = False
        return res

    #  关闭数据库连接
    def close(self):
        if(self._conn):
            try:
                if(type(self._cursor)=='object'):
                    self._cursor.close()
                if(type(self._conn)=='object'):
                    self._conn.close()
            except Exception:
                pass


if __name__ == '__main__':
    data = ReadPurchase()
    sql = data.get_purchase_order_id()
    d = Database()
    d.connmysql()
    res = d.fetch_all(sql)
    d.close()
    print(res[0][r'id'])
