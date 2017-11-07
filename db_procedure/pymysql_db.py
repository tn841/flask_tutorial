#-*- coding:utf-8 -*-
import pymysql


class DBManager:
    __connection = None
    cursor = None

    @staticmethod
    def init():
        print "init()"
        DBManager.__connection = pymysql.connect(host='localhost',
                                                 user='root',
                                                 password='rootroot',
                                                 db='test',
                                                 charset='utf8mb4',
                                                 cursorclass=pymysql.cursors.DictCursor)

        DBManager.cursor = DBManager.__connection.cursor()




