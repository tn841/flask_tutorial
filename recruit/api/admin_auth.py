#-*- coding:utf-8 -*-
'''
Created on 2017. 12. 19.

@author: tn841
'''
from flask.blueprints import Blueprint
from flask.globals import request
from recruit_base import dao
from flask.helpers import flash, url_for
from werkzeug import redirect
from flask_login.utils import login_user, current_user, logout_user
from db.user import User
from flask_login.login_manager import LoginManager
from recruit_base import app, try_except, admin_check
from mylogger import logger


admin_auth_api=Blueprint("admin_auth_api", __name__)

#Flask-Loing 모듈
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'admin_view.admin_login'
login_manager.login_message = "관리자 로그인이 필요합니다."

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


@admin_auth_api.route("/admin_login_action", methods=["POST"])
def admin_login():
    id = request.form['id'] if 'id' in request.form else ''
    pwd = request.form['pwd'] if 'pwd' in request.form else ''
    
    ###############
    cursor = dao.get_conn().cursor()
    query_str="select * from recruit_user where user_email like '%s'" % (id)
    cursor.execute(query_str)
    result=cursor.fetchone()
    cursor.close()
    ###############
    if result:
        if result[3] == pwd:
            login_user(User(id, name=result[2], auth=True, no=result[0]))
            flash("로그인 완료")
            return redirect(url_for('admin_view.admin_main'))
        else:
            flash("아이디 또는 비밀번호가 잘못되었습니다.")
            return redirect(url_for('admin_view.admin_main'))
    else:
        flash("아이디 또는 비밀번호가 잘못되었습니다.")
        return redirect(url_for('admin_view.admin_main'))
    
@admin_auth_api.route("/admin_logout_action")
@admin_check
def logout():
    current_user.authenticated = False
    logout_user()
    flash("로그아웃 되었습니다.")
    return redirect(url_for("admin_view.admin_main"))
    
    
    
    
    
    
    
    
    