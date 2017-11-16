# -*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.globals import current_app, request
from flask.templating import render_template
from flask_login.utils import login_required

from db.database import DBManager
from mylogger import logger

board_view = Blueprint("board_view", __name__)

@board_view.route("/common_board")
def common_board():

    try:
        cursor = DBManager.conn.cursor()
        cursor.callproc("select_post_list", (0,5,1))
        result = cursor.fetchall()
        cursor.close()
        logger.info(str(result))

        cursor = DBManager.conn.cursor()
        cursor.callproc("select_post_list", (0, 5, 1))
        result = cursor.fetchall()
        cursor.close()

        return render_template("/board/common_board.html", post_list=result)
    except Exception as e:
        raise e


@board_view.route("/member_board")
@login_required
def member_board():
    try:
        cursor = DBManager.conn.cursor()
        cursor.callproc("select_post_list", (0, 5, 2))
        result = cursor.fetchall()
        cursor.close()
        logger.info(str(result))

        cursor = DBManager.conn.cursor()
        cursor.callproc("select_post_list", (0, 5, 2))
        result = cursor.fetchall()
        cursor.close()
        return render_template("/board/member_board.html", post_list=result)
    except Exception as e:
        raise e

@board_view.route("/admin")
@login_required
def admin():
    return render_template("/board/admin.html")
