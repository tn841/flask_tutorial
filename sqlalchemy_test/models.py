#-*- coding:utf-8 -*-

from sqlalchemy import Column, Integer, String  #sqlalchemy패키지에서 필요한 클래스 import
from database import Base       #database.py의 Base 객체 import

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name,)


