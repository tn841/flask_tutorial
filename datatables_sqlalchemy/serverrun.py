#-*- coding:utf-8 -*-

from flask import Flask, redirect
from sqlalchemy.engine import create_engine

from controller import *
from datatables_blueprint import datatables_app
from datatables_sqlalchemy.DBManager import DBManager

app = Flask(__name__)

app.register_blueprint(datatables_app)



@app.route('/')
def index():
    return redirect('/datatables')

if __name__ == '__main__':
    DBManager.init();
    app.run(port=2323, debug=True)