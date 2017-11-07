#-*- coding:utf-8 -*-

import sys
from flask import Flask, request, redirect, make_response
from datetime import datetime



reload(sys)
sys.setdefaultencoding('utf-8')

def dateKoreanType(date_format, str):
    return datetime.strptime(str, date_format)





app = Flask(__name__)

@app.route('/')
def index():
    return "TEST"

@app.route("/board", methods=['GET', 'POST'])
def board():
    if request.method == 'GET':
        return "query string 값은 %s" % request.args.get('name','값을 입력하세요', type=int)
    elif request.method == 'POST':
        return "form 값은 %s" % request.form.get("name")

@app.route("/datetime", methods=['GET'])
def datetime():
    str = request.values.get("date", "2017-01-01")
    print str
    #dt = dateKoreanType("%Y-%m-%d")

    #print(request.values.get("date", "2011-01-01", type=DateType("%Y-%m-%d")))
    return 'test'

@app.route("/cookie")
def cookie():
    print(request.cookies)
    return ""

@app.route("/cookie_set")
def cookie_set():
    redirect_to_cookie = redirect("/cookie")
    resp = make_response(redirect_to_cookie)
    resp.set_cookie('key', value='value')
    return resp

@app.route("/url_ruless")
def url_rule():
    return str(request.url_rule)

@app.route("/view_args/<var>")
def view_args(var):
    return str(request.view_args)



app.run(port=1111, debug=True)