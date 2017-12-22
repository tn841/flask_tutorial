#-*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.globals import request, g
from flask.helpers import flash, url_for
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from mylogger import logger
from recruit_base import try_except, dao

register_api = Blueprint("register_api", __name__)

@register_api.route("/register_action", methods=["POST"])
@try_except
def register_action():
    name = request.values.get("name").encode("utf-8") if "name" in request.values else ''
    email = request.values.get("email").encode("utf-8") if "email" in request.values else ''
    pwd = request.values.get("pwd") if "pwd" in request.values else ''
    hashed_pwd = generate_password_hash(pwd, salt_length=10)
    logger.info('register_action data : '+name+', '+email+', '+hashed_pwd)

    cursor = dao.get_conn().cursor()
    cursor.callproc("insert_r_user", (email, name, hashed_pwd, 0))
    cursor.execute("select @_insert_r_user_3")
    result = cursor.fetchone()
    cursor.close()
    g.conn.commit()
    last_id = result[0]
    logger.info("insert result (last_id) : %s" % (last_id))

    msg = ""
    if result[0] > 0 :
        msg = name+"님 가입 성공, 로그인 하세요."
    else:
        msg = "가입 실패"
    flash(msg)
    return redirect(url_for('main_view.index'))