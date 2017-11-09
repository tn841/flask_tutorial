#-*- coding:utf-8 -*-
from datetime import datetime

from flask import Flask, redirect
from flask.helpers import send_from_directory
from flask.templating import render_template
import xlsxwriter
from sqlalchemy.engine import create_engine

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/do')
def do():
    #엑셀로 저장할 데이터
    expenses = (
        ['rent', 1000],
        ['gas' , 100],
        ['food', 300],
        ['gym', 50]
    )

    #workbook객체를 만들고 worksheet를 추가한다.
    date_string = datetime.now().strftime('%Y%m%d%H%M%S')

    workbook = xlsxwriter.Workbook('./resources/%s.xlsx' % (date_string))
    worksheet = workbook.add_worksheet('tutorial')

    #데이터를 채워넣기 시작할 row, col 설정, 인덱스는 0부터 시작, A1셀은 (0,0)이다.
    row = 0
    col = 0

    #데이터를 iterating하면서 worksheet에 데이터를 쓴다.
    for item, cost in expenses:
        worksheet.write(row, col, item)
        worksheet.write(row, col + 1, cost)
        row += 1

    #기타 작업
    worksheet.write(row, 0, 'Total')
    worksheet.write(row, 1, '=sum(B1:B4)')

    workbook.close()

    return send_from_directory('./resources','%s.xlsx' % (date_string), as_attachment=True)

@app.route("/db")
def db():
    #Xlsxwrite
    date_string = datetime.now().strftime('%Y%m%d%H%M%S')
    workbook = xlsxwriter.Workbook('./resources/%s.xlsx' % date_string)
    worksheet = workbook.add_worksheet('book_data')

    s_row = 2
    s_col = 1

    # DB연결
    engine = create_engine("mysql+pymysql://root:rootroot@localhost/test")
    conn = engine.raw_connection()
    cursor = conn.cursor()

    cursor.callproc('select_all_books')
    data = cursor.fetchall()

    worksheet.write(s_row-1, 1, 'book id')
    worksheet.write(s_row-1, 2, 'book name')
    worksheet.write(s_row-1, 3, 'book price')
    worksheet.write(s_row-1, 4, 'book type')

    for row_data in data:
        for col_data in row_data:
            worksheet.write(s_row, s_col, col_data)
            s_col += 1
        s_col = 1
        s_row += 1

    worksheet.write(s_row, 2, 'Total')
    worksheet.write(s_row, 3, '=sum(D3:D12)')
    worksheet.write(s_row, 4, '=counta(E3:E12)')

    workbook.close()

    return send_from_directory('./resources', '%s.xlsx' % date_string, as_attachment=True)


if __name__ == '__main__':
    app.run(port=2323, debug=True)