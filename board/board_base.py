#-*- coding:utf-8 -*-
import datetime
import os, sys

from flask import Flask
from flask.globals import g

from mylogger import logger

reload(sys)
sys.setdefaultencoding("utf-8")

#flask 객체 생성
app = Flask(__name__)

#config 설정
app.config.from_json('./app_config.conf')
logger.info(str(app.config.copy()))

#세션 설정
app.permanent_session_lifetime = datetime.timedelta(minutes=30)
#기본 설정으로 flask의 session을 사용하도록 'app_config.conf'에 설정해놓음
#직접 구현한 serverside session을 사용할 경우 app.session_interface = MySessionInterface()와 같이 설정한다.

#로깅 설정
#mylogger.py 모듈을 그때그때 import 하여 로깅

#데이터베이스 설정
db_user = 'root'
db_passwd = 'webdev1!'
db_host = '10.10.1.175'
db_schema = 'sumin'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+db_user+':'+db_passwd+'@'+db_host+'/'+db_schema+'?charset=utf8'
app.config['SESSION_TYPE'] = 'sqlalchemy'
from db.database import DBManager
DBManager(app.config['SQLALCHEMY_DATABASE_URI'])



basedir = os.path.dirname(os.path.abspath(__file__))

#api 등록
from api.auth import auth_api
from api.register import register_api
from api.board import board_api
from api.post import post_api
app.register_blueprint(auth_api)
app.register_blueprint(register_api)
app.register_blueprint(board_api)
app.register_blueprint(post_api)

#뷰함수 등록
from views.main import main_view
from views.auth import auth_view
from views.register import register_view
from views.board import board_view
from views.post import post_view
app.register_blueprint(main_view)
app.register_blueprint(auth_view)
app.register_blueprint(register_view)
app.register_blueprint(board_view)
app.register_blueprint(post_view)

#기타 설정

#app 전역에서 호출 가능한 util_func() 정의
@app.context_processor
def util_func():

    def get_board_list():
        try:
            cursor = DBManager.conn.cursor()
            cursor.callproc('select_board_list')
            result = cursor.fetchall()
            cursor.close()
            logger.info(str(result))
            b_list = []
            for b_id, b_name, b_type, b_url in result:
                b_list.append([b_name, b_type, b_url])
            logger.info(str(b_list))
            return b_list
        except Exception as e:
            raise e

    return dict(board_list=get_board_list)



