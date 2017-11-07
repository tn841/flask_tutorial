#-*- coding:utf-8 -*-

from photolog.model import Base
from sqlalchemy import Column, Integer
from sqlalchemy.sql.sqltypes import String


class User(Base):
    __tablename__ = 'users'

    #columns
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=False)
    password = Column(String(100), unique=False)

    #다른 테이블과의 관계 표기 가능...
    #photo = reationship()

    def __init__(self, name, email, password):
        self.username = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r %r>' % (self.username, self.email)
