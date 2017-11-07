#-*- coding:utf-8 -*-

'''
1. DB연결을 담당하는 class
'''
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker


class DBManager:
    __engine = None
    __session = None


    @staticmethod   #클래스에서 오직 한번만 실행하는 정적 메소드
    def init(db_url, db_log_flag_True):
        DBManager.__engine = create_engine(db_url, echo=db_log_flag_True)
        DBManager.__session = scoped_session(sessionmaker(bind=DBManager.__engine, autocommit=False, autoflush=False))

        global dao
        dao = DBManager.__session

    @staticmethod
    def init_db():
        from photolog.model import *
        from photolog.model import Base
        Base.metadata.create_all(bind=DBManager.__engine)

dao = None