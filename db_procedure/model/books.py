#-*- coding:utf-8 -*-
from model import Base
from sqlalchemy.dialects.mysql.types import DOUBLE
from sqlalchemy.sql.schema import Column
from sqlalchemy import CHAR, VARCHAR


class Books(Base):
    __tablename__='books'

    bookID = Column(CHAR(5), primary_key=True)
    bookName = Column(VARCHAR(50), unique=True)
    bookOriginPrice = Column(DOUBLE)
    bookType = Column(VARCHAR(10), nullable=False)

    def __init__(self, name, price, btype):
        self.bookName = name
        self.bookOriginPrice = price
        self.bookType = btype

    def __repr__(self):
        return '<Books %r %r>' % (self.bookName, self.bookOriginPrice, self.bookType)
