# -*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.globals import request, session
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login.login_manager import LoginManager
from board_base import app
from flask_login.utils import login_user, logout_user, current_user, login_required, login_fresh
from mylogger import logger
from db.user import User
from werkzeug.utils import redirect

auth_api = Blueprint("auth_api", __name__, url_prefix='/api')

#Flask-Login 모듈
login_manager = LoginManager()  # 로그인/로그아웃 관련 세션을 관리해주는 flask-login 모듈 객체 생성
login_manager.init_app(app)     # flask객체와 연동

#인증되지 않은 사용자가 @login_required 페이지 접속을 시도할 시 redirect할 페이지 설정
login_manager.login_view = 'auth_view.login'    
login_manager.login_message = "로그인이 필요합니다."

@login_manager.user_loader      # 세션에 저장된 ID에 해당하는 user객체를 반환하는 callback 메소드, 유효하지 않은 ID일 경우 None을 반환한다.
def load_user(id):
        logger.info("load_user(), session:"+str(session))
        try:
            from db.database import DBManager
            cursor = DBManager.conn.cursor()
            cursor.callproc('get_user_by_id', (id,))  # argument 1개일 때도 ,하나 붙여줘야 제대로 인식함.
            r = cursor.fetchall()
            cursor.close()

            if r : #id가 존재
                return User(id, name=r[0][2], auth=True)
            else:
                return None
        except Exception as e:
            logger.info(str(e))
            raise e
        finally:
            cursor.close()




@auth_api.route('/login', methods=['POST'])
def api_login():
    id = request.values.get('id') if "id" in request.form else None
    pw = request.values.get('pw') if "pw" in request.form else None
    logger.info("id : "+id)
    try:
        from db.database import DBManager   # DB관련 모듈 import
        cursor = DBManager.conn.cursor()    # cursor 객체를 얻는다.
        cursor.callproc('get_user_by_id', (id,))    #argument 1개일 때도 ,하나 붙여줘야 제대로 인식함.
        r = cursor.fetchall()
        cursor.close()
        logger.info("유저 정보 : "+str(r))

        if r:
            #id 존재
            logger.info("pw 체크 : "+ r[0][4])
            if r[0][4] == pw:
                session['user_id'] = id

                # 아이디와 비밀번호가 일치하면 로그인 처리
                # 직접 정의한 'User'클래스의 객체를 인자로 넘겨준다.
                login_user(User(id, name=r[0][2], auth=True))

                flash("로그인 되었습니다.")
                return redirect(url_for('main_view.index'))
            else:
                flash("아이디 또는 비밀번호를 확인하세요.")
                return redirect(url_for('auth_view.login'))
        else:
            flash("아이디 또는 비밀번호를 확인하세요.")
            return redirect(url_for('auth_view.login'))

    except Exception as e:
        logger.info(str(e))
    finally:
        cursor.close()

@auth_api.route('/logout', methods=['GET'])
@login_required
def api_logout():
    try:
        current_user.authenticated = False
        tmp_id = session['user_id']
        logout_user()
        session.clear()
        flash(tmp_id+"님 로그아웃 되었습니다.")
        return redirect(url_for("main_view.main"))
    except Exception as e:
        logger.info(str(e))