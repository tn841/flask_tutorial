#-*- coding:utf-8 -*-
from functools import wraps

from flask.globals import request, session
from flask.helpers import url_for
from flask.templating import render_template
from photolog.photolog_blueprint import photolog
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from wtforms import validators
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.form import Form

from photolog.database import dao
from photolog.model.user import User

from photolog.controller.login import login_required


def __get_user(name):
    try:
        return dao.query(User).filter_by(username=name).first()
    except Exception as e:
        print str(e)
        raise e




@photolog.route("/register")
def regist_user():
    form = Register_user_form(request.form)
    return render_template('/register_user.html', form=form)


@photolog.route("/register", methods=['POST'])
def register_action():
    form = Register_user_form(request.form)
    error_msg = None
    if form.validate():
        name = form.username.data
        password = form.password.data
        email = form.email.data

        #id 중복 확인
        if __get_user(name):
            error_msg = name+"은 이미 가입된 ID입니다."
            return render_template('/register_user.html', error=error_msg, form=form)

        try:
            #DB작업
            new_user = User(name, email, generate_password_hash(password))
            dao.add(new_user)
            dao.commit()

        except Exception as e:
            error = "DB error : " + str(e)
            print error
            dao.rollback()
            raise e
        return redirect(url_for('.login_form_page', regist_user=name))
    return render_template('/register_user.html', form=form, error=error_msg)


@photolog.route("/member")
@login_required
def member():
    return 'only memeber'

class Register_user_form(Form):
    username = StringField('username', [validators.required("사용자이름을 입력하세요.")])
    email = StringField('email', [validators.required("이메일을 입력하세요..")])
    password = PasswordField('password', [validators.required("비밀번호를 입력하세요.")])
    pass_confirm = PasswordField('pass_confirm',[validators.required("비밀번호 확인"), validators.equal_to('password', message="비밀번호가 일치하지 않습니다.")])
    submit = SubmitField('submit')