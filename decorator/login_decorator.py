#-*- coding:utf-8 -*-

from functools import wraps
from flask import Flask, session, request, redirect, url_for
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def login_required(f):
    @wraps(f)   #디버깅을 위해 @wraps 데코레이터를 추가한다.
    def decorated_function(*args, **kwargs):
        if session.get('user', None) is None:   #세션에 'user'값이 없으면, 즉 로그인이 되어 있지않으면 'index'페이지로 redirect
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)   #로그인이 되어있으면 view함수 그대로 실행
    return decorated_function


app = Flask("__name__")
app.secret_key = '111'

@app.route("/")
def index():
    return "로그인이 필요합니다."

@app.route("/set_session")
def set_session():
    session['user'] = 'sumin'
    return redirect(url_for('member_page'))

@app.route("/member")
@login_required #로그인 여부를 판단하는 사용자정의 데코레이터
def member_page():
    return "회원만 볼 수 있음"

if __name__ == '__main__':
    app.run(debug=True, port=2323)