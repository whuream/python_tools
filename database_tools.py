# encoding: utf-8
__author__ = 'tong'


import MySQLdb

import logging
logger = logging.getLogger(__name__)


class ConnDB:
    def __init__(self, sql_server, cursorclass=None):
        self.sql_server = sql_server
        self.cursorclass = cursorclass

    def __enter__(self):
        self.conn = MySQLdb.connect(host=self.sql_server['host'],
                                    user=self.sql_server['user'],
                                    passwd=self.sql_server['password'],
                                    db=self.sql_server['database'],
                                    port=int(self.sql_server['port']),
                                    charset='utf8')
        self.cursor = self.conn.cursor(self.cursorclass)
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    ALIMUSIC_DATAIN = {'host': '10.189.196.127',
                   'user': 'ALIMUSIC_DATAIN_APP',
                   'password': '123456',
                   'database': 'ALIMUSIC_DATAIN_APP',
                   'port': '3306'}

    sql = 'select * from spider_artist'

    with ConnDB(ALIMUSIC_DATAIN) as cursor:
        sql_ret = cursor.execute(sql)

        print(sql_ret)

        sql_data = cursor.fetchall()

        print(sql_data)
