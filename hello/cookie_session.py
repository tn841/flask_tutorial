#-*- coding:utf-8 -*-

import sys
from flask import Flask, make_response, request, session
from datetime import timedelta

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.secret_key = 'my_secret_key'
app.config.update(
    SESSION_COOKIE_NAME='my_session_name',
    PERMANENT_SESSION_LIFETIME=timedelta(30)
)

@app.route("/")
def index():
    return '<h1>cookie & session tutorial</h1><hr>'


@app.route("/cookie_set")
def cookie_set():
    resp = make_response("쿠키에 값을 설정했습니다.")
    resp.set_cookie("cookie_key", "cookie_value")
    return resp

@app.route("/cookie_clear")
def cookie_clear():
    resp = make_response("쿠키정보를 지웁니다.")
    resp.set_cookie("cookie_key", expires=0)
    return resp

@app.route("/cookie_confirm")
def cookie_confirm():
    return request.cookies.get('cookie_key', '없음')


@app.route("/session_set")
def session_set():
    session['S_ID'] = 'session_value'
    return "세션 설정 완료"


if __name__ == '__main__':
    app.run(debug=True, port=3333)


