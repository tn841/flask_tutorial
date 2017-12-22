#-*-coding:utf-8-*-
from flask.globals import g
from sqlalchemy.engine import create_engine


class RecruitDB:
    def __init__(self, url):
        self.engine = create_engine(url)

    def get_conn(self):
        if not hasattr(g, 'conn'):
            self.conn = self.engine.raw_connection()
            g.conn = self.conn

        return g.conn