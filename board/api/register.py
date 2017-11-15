# -*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.globals import request
from flask.helpers import make_response, url_for, flash
from flask.templating import render_template
from mylogger import logger
from werkzeug.utils import redirect

register_api = Blueprint('register_api',__name__,url_prefix="/api")

@register_api.route("/register", methods=['POST'])
def register_action():
    form = request.form
    id = request.values.get('id') if 'id' in request.values else None
    name = request.values.get('name') if 'name' in request.values else None
    email = request.values.get('email') if 'email' in request.values else None
    pw = request.values.get('pw') if 'pw' in request.values else None
    pw_check = request.values.get('pw_check') if 'pw_check' in request.values else None

    try:
        from db.database import DBManager
        cursor = DBManager.conn.cursor()

        cursor.callproc('insert_user', (id, name, email, pw, 0))
        cursor.execute('select @_insert_user_4')
        result = cursor.fetchone()
        cursor.close()
        logger.info("insert result : " + str(result))
        if int(result[0]) == 0:
            flash("회원가입 되었습니다. 로그인 하세요.")
            return redirect(url_for('auth_view.login'))
        flash("이미 가입된 아이디 입니다.")
        return redirect(url_for('register_view.reigster_form'))
    except Exception as e:
        logger.info(str(e))





