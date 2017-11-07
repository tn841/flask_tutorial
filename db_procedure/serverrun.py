#-*- coding:utf-8 -*-
import pymysql
from flask import Flask

from database import DBManager

app = Flask(__name__)

@app.route('/')
def index():
    return 'procedure test'

@app.route('/procedure/<num1>/<num2>')
def procedure_test(num1, num2):
    cursor = DBManager.conn.cursor()
    try:
        cursor.callproc('multiply', (num1,num2,0))
        cursor.execute('select @_multiply_2')
        results = list(cursor.fetchone())
        return str(results[0])
    finally:
        cursor.close()

@app.route('/insertbook')
def insertbook():
    cursor = DBManager.conn.cursor()
    try:
        cursor.execute('select books.bookID from books order by bookID * 1 DESC limit 1')
        last_idx = int(cursor.fetchone()[0])
        last_idx = last_idx+1
        cursor.callproc('INSERT_BOOK', (last_idx, 'newbook', 32000, 'novel', 0))
        cursor.execute('select @_INSERT_BOOK_0, @_INSERT_BOOK_4')
        result = cursor.fetchone()
        return "책 insert 결과 : "+str(result)
    finally:
        cursor.close()

if __name__ == '__main__':
    DBManager.init()
    app.run(port=2323, debug=True)