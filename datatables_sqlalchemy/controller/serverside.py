#-*- coding:utf-8 -*-
from datatables import DataTables
from datatables_blueprint import datatables_app
from flask.globals import request
from flask.helpers import make_response
from flask.json import jsonify
from flask.templating import render_template
from datatables_sqlalchemy.DBManager import DBManager
from datatables_sqlalchemy.model.Book import Book


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
        cursor.callproc('select_all_books')
        data = cursor.fetchall()
        tabledata = {}
        tabledata["draw"] = 1
        tabledata["recordsTotal"] = len(data)
        tabledata["data"] = data
        print str(tabledata)

        #datatables 모듈을 이용해서 적절한 형식으로 데이터를 반환한다.
    except Exception as e:
        tabledata = {"error" : e}
    finally:
        cursor.close()
        return make_response(jsonify(tabledata))


