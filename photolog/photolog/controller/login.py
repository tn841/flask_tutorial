#-*- coding:utf-8 -*-

'''
- 로그인 관련 로직을 처리하는 controller
'''
from functools import wraps

from flask.globals import request, session
from flask.helpers import flash, url_for
from flask.templating import render_template
from photolog.photolog_blueprint import photolog
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect
from wtforms import validators
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField
from wtforms.form import Form

from photolog.database import dao

from photolog.model.user import User


@photolog.teardown_request
def close_db_session(exception=None):
    "요청 처리 완료 후 DB 세션 닫기"
    print 'close_db_session()'
    try:
        dao.remove()
    except Exception as e:
        print str(e)
        raise e


def login_required(func):
    @wraps(func)
    def deco_func(*args, **kwargs):
        try:
            session_key = request.cookies.get('session')

            is_login = False

            if session_key:
                is_login = True

            if not is_login:
                return render_template('/login.html', error='로그인이 필요합니다.')
            return func(*args, **kwargs)
        except Exception as e:
            print str(e)
            raise e

    return deco_func


@photolog.route('/')
def index():
    return render_template('/login.html')


@photolog.route('/login')
def login_form_page():
    form = LoginForm(request.form)
    new_user = request.values.get("regist_user", '')
    print new_user
    return render_template('/login.html', form= form, regist_user=new_user)

@photolog.route('/login', methods=['POST'])
def login_action():
    form = LoginForm(request.form)
    login_error = None

    if form.validate():
        session.permanent = True

        username = form.username.data
        password = form.password.data

        try:
            user = dao.query(User).filter_by(username=username).first()
        except Exception as e:
            print str(e)
            raise e

        if user:
            if not check_password_hash(user.password, password):
                login_error = '비밀번호가 틀렸습니다.'
            else:
                #session작업 완료 후 로그인 완료
                login_error = "session처리 후 로그인 완료"
                session['user_info'] = username
                return redirect(url_for('.index'))
        else:
            login_error = "ID가 존재하지 않습니다."

        return  render_template('/login.html', error=login_error, form=form)
    return render_template('/login.html', error=login_error, form=form)


@photolog.route('/logout')
def logout():
    session.clear()
    return render_template('/login.html', msg='성공적으로 로그아웃 되었습니다.')

class LoginForm(Form):
    username = StringField('username', [validators.required('이름을 입력해야합니다.')])
    password = PasswordField('password', [validators.required('비밀번호를 입력해야합니다.')])

