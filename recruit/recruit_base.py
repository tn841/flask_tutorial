# -*- coding:utf-8 -*-
from functools import wraps
from flask.app import Flask
import sys, os
from mylogger import logger
from flask.globals import g
from datetime import datetime
from flask_login.utils import current_user
from werkzeug import redirect
from flask.helpers import url_for, flash
from Tkconstants import CURRENT

reload(sys)
sys.setdefaultencoding("utf-8")

#flask 앱 생성
app = Flask(__name__)
logger.info("\n\n\n")
logger.info("===========================================================")
logger.info(">>> creating app..")


#recruit_conf 설정
app.config.from_json("recruit_conf.json")
logger.info(">>> app.confing : %s" % (str(app.config)))


#flask app context관리
@app.teardown_request
def db_close(e):
    if hasattr(g,"conn"):   #db_conntion이 있을 때만 close한다.
        #g.conn.commit()
        g.conn.close()
        logger.info( ">> db connection close - %s" % (g.conn))



#사용자 정의 데코레이터
def try_except(f):
    @wraps(f)
    def deco_func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.info("\n\n\n############exception############")
            logger.info(str(e))
            logger.info("#################################\n\n")
            raise e
    return deco_func

def admin_check(f):
    @wraps(f)
    def deco_func(*args, **kwargs):
        u_no = current_user.user_no if hasattr(current_user, 'user_no') else ''
        if str(u_no) == '1':
            return f(*args, **kwargs)
        else:
            flash("관리자 로그인이 필요합니다.")
            return redirect(url_for('admin_view.admin_main'))
    return deco_func



#전역 함수
def appliable_check(notice_no):
    ###################
    cursor = dao.get_conn().cursor()
    query_str="select n_s_date, n_e_date from recruit_notice where n_no = %s" % (notice_no)
    cursor.execute(query_str)
    logger.info(query_str)
    dates=cursor.fetchall()
    ###################
    
    if datetime.now() >= dates[0][0] and datetime.now() <= dates[0][1]:
        return True
    return False

#app 전역에서 호출 가능한 util_func() 정의 (template에서 사용하기 위해)
@app.context_processor
def util_func():

    def ymd_func(dt):
        return dt.strftime("%Y-%m-%d")

    return dict(datetime_func=ymd_func)


#DB conf
from db.RecruitDB import RecruitDB
db_user = app.config['DB_USER']
db_passwd = app.config["DB_PASSWD"]
db_host = app.config["DB_HOST"]
db_schema = app.config["DB_SCHEMA"]
db_url = 'mysql+pymysql://'+db_user+':'+db_passwd+'@'+db_host+'/'+db_schema+'?charset=utf8'
dao = RecruitDB(db_url)
logger.info(">>> DB connection : %s" % (str(dao)))

#blueprint 등록
from views.apply import apply_view
from views.auth import auth_view
from views.main import main_view
from views.register import register_view
from views.mypage import mypage_view
from views.notice import notice_view
from views.admin import admin_view

from api.apply import apply_api
from api.register import register_api
from api.auth import auth_api
from api.admin_auth import admin_auth_api
from api.admin_notice import admin_notice_api
from api.admin_resume import admin_resume_api

app.register_blueprint(main_view)
app.register_blueprint(apply_view)
app.register_blueprint(apply_api)
app.register_blueprint(register_view)
app.register_blueprint(register_api)
app.register_blueprint(auth_view)
app.register_blueprint(admin_view)

app.register_blueprint(auth_api)
app.register_blueprint(mypage_view)
app.register_blueprint(notice_view)
app.register_blueprint(admin_auth_api)
app.register_blueprint(admin_notice_api)
app.register_blueprint(admin_resume_api)

logger.info(">>> Blueprint setting. ")
logger.info("===========================================================")
