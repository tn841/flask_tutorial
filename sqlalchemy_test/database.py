#-*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker #세션객체 관리 클래스인 scoped_session, 세션생성 클래스인 sessionmaker
from sqlalchemy.ext.declarative import declarative_base #base declare 클래스를 반환

#DB에 접속할 engine객체를 선언, 접속할 URL, 접속 driver를 인자로 넘긴다.
engine = create_engine("mysql+pymysql://root:rootroot@localhost/test", echo=True, convert_unicode=True) #pip install pymysql로 mysql용 드라이버를 설치한 후,

#DB 조작을 수행할 session 객체, scoped_session은 세션을 관리하고, sessionmaker클래스는 DB engine을 인자로 받아 session을 생성한다.
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

#declarative_base() 메소드로부터 Base객체를 받는다.
#Base객체가 어떤 session을 사용할지 설정,
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models   #Base클래스를 상속받는 model객체가 있는 파일을 import한다.
    Base.metadata.create_all(bind=engine)   #Base.metadata.create_all() 메소드의 인자로 위에서 만든 engine객체를 넘겨주면 DB 테이블을 일괄적으로 생성한다.