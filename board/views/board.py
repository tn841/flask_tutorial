# -*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.globals import current_app, request, g
from flask.templating import render_template
from flask_login.utils import login_required

from db.database import DBManager
from mylogger import logger

board_view = Blueprint("board_view", __name__)

@board_view.route("/common_board")
#@board_view.route("/common_board/<cur_page>")
def common_board():
    return render_template("/board/common_board.html")
    # #page nation variables
    # per_page = current_app.config['PER_PAGE']
    # total_post_cnt = 0
    # total_page_cnt = 0
    #
    # print "per_page : %s, cur_page : %s" % (per_page, cur_page)
    #
    # try:
    #
    #     cursor = DBManager.conn.cursor()
    #     cursor.callproc("get_total_post_cnt", (1,))
    #     result = cursor.fetchone()
    #     cursor.close()
    #     print "common post total : %d" % (result)
    #
    #     total_post_cnt = result
    #     total_page_cnt = (total_post_cnt[0] / per_page) if (total_post_cnt[0] % per_page) == 0 else (total_post_cnt[0] / per_page) +1
    #     print "total_page_cnt : "+str(total_page_cnt)
    #
    #
    #
    #     cursor = DBManager.conn.cursor()
    #     start_n = (int(cur_page) -1) * per_page
    #     print "start_n : %d, end_n : %d" % (start_n, per_page)
    #     cursor.callproc("select_post_list", (start_n,per_page,1))
    #     result = cursor.fetchall()
    #     cursor.close()
    #     logger.info(str(result))
    #
    #
    #     return render_template("/board/common_board.html",
    #                            post_list=result,
    #                            post_cnt=total_post_cnt[0],
    #                            page_cnt=total_page_cnt,
    #                            cur_page=cur_page)
    # except Exception as e:
    #     raise e


@board_view.route("/member_board")
@board_view.route("/member_board/<cur_page>")
@login_required
def member_board(cur_page=1):
    return render_template("/board/member_board.html")
    # # page nation variables
    # per_page = current_app.config['PER_PAGE']
    # total_post_cnt = 0
    # total_page_cnt = 0
    #
    # try:
    #     cursor = DBManager.conn.cursor()
    #     cursor.callproc("get_total_post_cnt", (2,))
    #     result = cursor.fetchone()
    #     cursor.close()
    #     print "common post total : %d" % (result)
    #
    #     total_post_cnt = result
    #     total_page_cnt = (total_post_cnt[0] / per_page) if (total_post_cnt[0] % per_page) == 0 else (total_post_cnt[0] / per_page) + 1
    #     print "total_page_cnt : " + str(total_page_cnt)
    #
    #     cursor = DBManager.conn.cursor()
    #     start_n = (int(cur_page) - 1) * per_page
    #     print "start_n : %d, end_n : %d" % (start_n, per_page)
    #     cursor.callproc("select_post_list", (start_n, per_page, 2))
    #     result = cursor.fetchall()
    #     cursor.close()
    #     logger.info(str(result))
    #
    #     return render_template("/board/member_board.html",
    #                            post_list=result,
    #                            post_cnt=total_post_cnt[0],
    #                            page_cnt=total_page_cnt,
    #                            cur_page=cur_page)
    # except Exception as e:
    #     raise e

@board_view.route("/admin")
@login_required
def admin():
    return render_template("/board/admin.html")
