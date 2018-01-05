#-*- coding:utf-8 -*-
from datetime import datetime, timedelta
from crypto.library.hash import generate_hash
from flask.blueprints import Blueprint
from flask.globals import request, current_app
from flask.helpers import url_for, flash, make_response
from flask_login.login_manager import LoginManager
from flask_login.utils import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect
from mylogger import logger
from db.user import User
from recruit_base import app, try_except, dao

auth_api = Blueprint("auth_api", __name__, url_prefix='/api')

#Flask-Loing 모듈
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'auth_view.login_form'
login_manager.login_message = "로그인이 필요합니다."

@login_manager.user_loader
@try_except
def load_user(email):
    logger.info("load_user(%s)" % (email))
    cursor = dao.get_conn().cursor()
    cursor.execute("select * from recruit_user where user_email like '%s'" % (email))
    result = cursor.fetchone()

    if result[1] == email:
        return User(email, name=result[2], auth=True, no=result[0])
    else:
        return None



@auth_api.route('/login_action', methods=["POST"])
def login_action():
    email = request.values["email"] if "email" in request.form else ""
    pw = request.values["pwd"] if "pwd" in request.form else ""
    notice_no = request.values["notice_no"] if "notice_no" in request.values else ''
    rmb = request.values["rmb"] if "rmb" in request.form else ""

    print "rmb:"+str(rmb)



    cursor = dao.get_conn().cursor()
    cursor.execute("select * from recruit_user where user_email like '%s'" % (email))
    result = cursor.fetchone()
    cursor.close()

    logger.info("login_action, check email : "+str(result))

    try:
        if result:
            if check_password_hash(result[3], pw):
                login_user(User(email, name=result[2].decode('utf-8'), auth=True, no=result[0]))


                if notice_no != '':
                    return redirect(url_for('notice_view.notice_post', p_no=notice_no))
                else:

                    response = make_response(redirect(url_for("main_view.index")))
                    if rmb == 'on':
                        from aes_cipher import encrypt
                        expire_date = datetime.now() + timedelta(days=90)
                        enc_email = encrypt(current_app.config['SECRET_KEY'], email)
                        response.set_cookie('rmber', value=enc_email, expires=expire_date)
                    else:
                        response.set_cookie('rmber', expires=0)

                    flash("로그인 되었습니다.")
                    return response
            else:
                flash("아이디 또는 비밀번호가 일치하지 않습니다.")
                return redirect(url_for("auth_view.login_form"))
        else:
            flash("아이디 또는 비밀번호가 일치하지 않습니다.")
            return redirect(url_for("auth_view.login_form"))

    except Exception as e:
        logger.info(str(e))
        raise e

@auth_api.route('/logout_action', methods=["GET"])
@login_required
def logout_action():
    try:
        current_user.authenticated = False
        logout_user()
        flash("로그아웃 되었습니다.")
        return redirect(url_for("main_view.index"))
    except Exception as e:
        logger.info(str(e))
        raise e