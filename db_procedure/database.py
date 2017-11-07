#-*- coding:utf-8 -*-
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker




class DBManager:
    __engine = None
    conn = None
    session = None

    @staticmethod
    def init():
        print "DBManager.init()"
        DBManager.__engine = create_engine("mysql+pymysql://root:rootroot@localhost/test", echo=True)
        DBManager.session = scoped_session(sessionmaker(bind=DBManager.__engine, autocommit=False))
        DBManager.conn = DBManager.__engine.raw_connection()    # procedure를 사용하기위해 raw_conntion이 필요하다.

    @staticmethod
    def init_db():
        print "DBManager.init_db()"
        from model import *
        from model import Base

        Base.metadata.create_all(bind=DBManager.__engine)



