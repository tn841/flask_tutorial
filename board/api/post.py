# -*- coding: utf-8 -*-
from datetime import datetime

from flask.blueprints import Blueprint
from flask.globals import request

from db.database import DBManager
from flask.helpers import flash, url_for
from mylogger import logger
from werkzeug.utils import redirect

post_api = Blueprint("post_api", __name__)

@post_api.route("/insert_post_action", methods=['POST'])
def insert_post():

    data = request.values
    logger.info("form data : " + str(data))
    p_title = data.get('p_title') if data.get('p_title') else None
    p_body = data.get('p_body') if data.get('p_title') else None
    p_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    p_writer = data.get('p_writer') if data.get('p_writer') else None
    b_id = None
    if data.get('b_type') == 'common_board/':
        b_id = 1
    elif data.get('b_type') == 'member_board/':
        b_id = 2

    logger.info("post insert : "+str(p_title)+", "+str(p_body)+", "+str(p_date)+", "+str(p_writer)+", "+str(b_id))
    try:
        cursor = DBManager.conn.cursor()
        cursor.callproc('insert_post',(p_title, p_body, p_date, p_writer, b_id, 0))
        cursor.execute('select @_insert_post_5')
        result = cursor.fetchone()
        logger.info("post insert result : "+str(result[0]))
        if result[0] == 0:
            flash("글이 등록 되었습니다.")
            return redirect(url_for("board_view.common_board"))
        else:
            flash("글 등록과정에서 오류가 발생하였습니다.")
            return redirect(url_for("post_view.post_form"))
    except Exception as e:
        logger.info(str(e))
    finally:
        cursor.close()


