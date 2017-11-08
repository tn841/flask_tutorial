#-*- coding:utf-8 -*-
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker


class DBManager:
    engine = None
    conn = None
    session = None

    @staticmethod
    def init():
        print "DBManaer.init()"
        DBManager.engine = create_engine("mysql+pymysql://root:rootroot@localhost/test", echo=True)
        DBManager.session = scoped_session(sessionmaker(bind=DBManager.engine))

        from model import *
        from model import Base
        Base.metadata.create_all(bind=DBManager.engine)

        DBManager.conn = DBManager.engine.raw_connection()