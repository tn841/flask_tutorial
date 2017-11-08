#-*- coding:utf-8 -*-
from sqlalchemy.dialects.mysql.types import DOUBLE
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import CHAR, VARCHAR

from datatables_sqlalchemy.model import Base


class Book(Base):
    __tablename__ = "books"

    bookID = Column(CHAR, primary_key=True)
    bookName = Column(VARCHAR, nullable=False)
    bookOriginPrice = Column(DOUBLE)
    bookType = Column(VARCHAR, nullable=False)

    def __init__(self, id, name, price, type):
        self.bookID = id
        self.bookName = name
        self.bookOriginPrice = price
        self.bookType = type


    def __repr__(self):
        return "<Book %r %r %r>" % (self.bookName, self.bookOriginPrice, self.bookType)