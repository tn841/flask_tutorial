#-*- coding:utf-8 -*-

import sys
from datetime import datetime
from flask import Flask, redirect, session
from flask.globals import request
from flask.helpers import flash
from flask.templating import render_template
from functools import wraps
from MySessionInterface import MySimpleCacheSessionInterface
# from cache_session import SimpleCacheSessionInterface
from MySessionInterface2 import SimpleCacheSessioninterface

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = 'my_session'
app.config['PERMANENT_SESSION_LIFETIME'] = 1 * 60
# app.session_interface = MySessionInterface()
app.session_interface = MySimpleCacheSessionInterface()
# app.secret_key = 'asaaaaadf'

def login_required(f):
    '''
        로그인 상태 체크 데코레이터
    :param f:
    :return:
    '''

    @wraps(f)
    def deco_func(*args, **kwargs):
        try:
            session_key = request.cookies.get(app.config['SESSION_COOKIE_NAME'])

            is_login = False
            print str(session.sid) + " == " + str(session_key) + " : " + str(session.sid == session_key)
            print 'session.__contains__("userid") : ' + str(session.copy())
            if session.sid == session_key and session.__contains__('userid'):
                is_login = True

            if not is_login:
                print '로그인 필요'
                flash("login please.")
                return redirect('/')

            return f(*args, **kwargs)
        except Exception as e:
            print '에러 : ' + str(e)
            raise e
    return deco_func




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/<user>')
def do_login(user):
    session.permanent = True
    session['userid'] = user
    session['login_time'] = datetime.now()
    print('로그인 완료, userid : '+user)
    return redirect('/member_page')

@app.route('/logout')
def do_logout():
    print '>> 로그아웃 요청이 들어옴,, sesseion을 clear한다.'
    session.clear()
    flash('logout success')
    return redirect('/')

@app.route('/member_page')
@login_required
def only_memeber():
    return '회원만 접근가능한 페이지 입니다.' + session.get('userid')+ '님 반갑습니다. <br> 세션 만료시간 : '+ str(session.copy())
    

if __name__ == '__main__':
    app.run(port=2323, debug=True)