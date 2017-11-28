# -*- coding:utf-8 -*-
from flask.globals import g
from sqlalchemy.engine import create_engine
from mylogger import logger

class DBManager:

    def __init__(self, url):
        self.engine =  create_engine(url)
        logger.info("DBManager.__init__()")

    def get_conn(self):
        print 'get_conn(), g.conn : %s' % (str(hasattr(g, 'conn')))
        if not hasattr(g, 'conn'):
            self.conn = self.engine.raw_connection()
            g.conn = self.conn
            print ">> connection open() : "+str(g.conn)

        logger.info("DBManager.open()")
        return g.conn;