# -*- coding:utf-8 -*-
from sqlalchemy.engine import create_engine
from mylogger import logger

class DBManager:
    engine = None
    conn = None

    @staticmethod
    def __init__(url):
        DBManager.engine =  create_engine(url)
        DBManager.conn = DBManager.engine.raw_connection()
        logger.info("DBManager.__init__()")