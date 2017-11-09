#-*- coding:utf-8 -*-
import datetime

import xlsxwriter
from datatables_blueprint import datatables_app
from datetime import datetime
from flask.helpers import make_response, send_from_directory
from flask.json import jsonify
from flask.templating import render_template
from datatables_sqlalchemy.DBManager import DBManager


@datatables_app.route("/")
def index():
    return render_template('/index.html')

@datatables_app.route("/get_data", methods=['POST'])
def get_data_func():
    conn = DBManager.conn
    cursor = conn.cursor()
    try:
        cursor.callproc('multiply', (2,3,0))
        cursor.execute('select @_multiply_2')
        ddd = cursor.fetchone()
        data = {"key_data" : ddd}
    except Exception as e:
        data = {"key_data": str(e)}
    finally:
        cursor.close()
        return make_response(jsonify(data))

@datatables_app.route("/get_table_data", methods=['POST', 'GET'])
def get_table_data_func():
    conn = DBManager.conn
    cursor = conn.cursor()
    try:
        cursor.callproc('select_all_books') #book데이터를 가져오는 프로시저 호출
        data = cursor.fetchall()

        #datatables lib에서 사용하는 json형식에 맞게 dictionary생성
        tabledata = {}
        tabledata["draw"] = 1
        tabledata["recordsTotal"] = len(data)
        tabledata["data"] = data
        print str(tabledata)

        #datatables 모듈을 이용해서 적절한 형식으로 데이터를 반환한다.
        #sqlalchemy ORM을 활용할 수 있다.
    except Exception as e:
        tabledata = {"error" : e}
    finally:
        cursor.close()
        return make_response(jsonify(tabledata))    #json형식으로 데이터를 반환한다.


@datatables_app.route("/excel_download")
def excel_donwload():
    # Xlsxwrite
    date_string = datetime.now().strftime('%Y%m%d%H%M%S')
    workbook = xlsxwriter.Workbook('./resources/%s.xlsx' % date_string)
    worksheet = workbook.add_worksheet('book_data')

    s_row = 2
    s_col = 1

    # DB연결
    conn = DBManager.conn
    cursor = conn.cursor()

    cursor.callproc('select_all_books')
    data = cursor.fetchall()
    cursor.close()

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


