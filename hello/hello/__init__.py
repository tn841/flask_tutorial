#-*- coding:utf-8 -*-

from flask import Flask, make_response

app = Flask(__name__)

@app.before_first_request
def before_first_request():
    print "첫 요청 전에만 실행"

@app.before_request
def before_request():
    print "모든 요청 처리 전에 실행"

@app.after_request
def after_request(resp):
    print "모든 요청 처리 후 실행"
    return resp

@app.teardown_request
def teardown_request(resp):
    print "모든 요청 처리 후 실행(오류 발생 시에도 동작)"
    return resp

@app.route('/')
def hello():
    return 'hello flask'

@app.route('/tuple')
def tuple():
    return make_response(('Tuple custom response', 'OK', {'response_method':'Tuple Response'}))

@app.route("/method", methods=['POST'])
def method():
    return 'POST method'

@app.route("/variable/<var>")
def variable(var):
    return 'var = %d' % int(var)

@app.route("/board/<id>")
@app.route("/board", defaults={"id":11})    #초기값 지정
def board(id):
    return "%d 번째 board를 보여준다." % int(id)