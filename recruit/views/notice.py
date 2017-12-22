#-*- coding:utf-8 -*-
from time import strptime

from flask.blueprints import Blueprint
from flask.templating import render_template
from flask_login.utils import current_user
from datetime import datetime
from mylogger import logger
from recruit_base import try_except, dao, appliable_check
from flask.helpers import flash, url_for
from werkzeug import redirect
from flask.globals import request

notice_view = Blueprint("notice_view", __name__)

@notice_view.route("/notice")
@notice_view.route("/notice/<page>")
@try_except
def notice_board(page=1):
    
    n_type=request.values['n_type'] if 'n_type' in request.values else '1'
    
    if int(n_type) < 1 or int(n_type) > 4:
        flash("잘못된 접근입니다.")
        return redirect(url_for("main_view.index"))
    
    
    cur_dt=datetime.now().strftime("%Y-%m-%d")
    query_str="select * from recruit_notice"
    if n_type == '3': #마감된
        query_str = query_str+" where '%s' > n_e_date" % (cur_dt)
    elif n_type == '4': #예정
        query_str = query_str+" where '%s' < n_s_date" % (cur_dt)
    elif n_type == '2': #진행중
        query_str = query_str+" where '%s' >= n_s_date and '%s' <= n_e_date" % (cur_dt, cur_dt)
    #################
    cursor = dao.get_conn().cursor()
    cursor.execute(query_str)
    result = cursor.fetchall()
    cursor.close()
    #################
    
    per_page = 5
    total_post = len(result)
    cur_page = (int(page)-1) * 5
    total_page = 0
   
    
    if int(total_post) % int(per_page) == 0:
        total_page = (int(total_post)/int(per_page))
    else:
        total_page = (int(total_post)/int(per_page)) + 1
    

    query_str = query_str + " order by n_no DESC limit %s, %s" % (str(cur_page), str(per_page))
    #################
    cursor = dao.get_conn().cursor()
    cursor.execute(query_str)
    result = cursor.fetchall()
    cursor.close()
    #################
    
    

    logger.info("notice_board view data : "+str(result))
    return render_template("/notice/notice_board.html", data=result, per_page=per_page, total_post=total_post, cur_page=cur_page, total_page=total_page)


@notice_view.route("/notice_view/<p_no>")
@try_except
def notice_post(p_no):
    
    if not appliable_check(p_no):
        flash("지원가능한 기간이 아닙니다.")
        return redirect(url_for("notice_view.notice_board"))
    
    cursor = dao.get_conn().cursor()
    cursor.execute("select * from recruit_notice where n_no = %s" % (p_no))
    result = cursor.fetchone()
    cursor.close()

    if not current_user.is_authenticated:
        result = result + ('login',)
        return render_template("/notice/notice_post.html", data=result)


    #이미 해당공고에 대한 이력서가 있으면 '수정하기'버튼을 보여준다.
    cursor = dao.get_conn().cursor()
    cursor.execute("select * from resume where r_notice_no = %s and r_writer_no = %s " % (p_no, current_user.user_no))
    result2 = cursor.fetchone();

    if result2:
        result = result + ('modify',)
    else:
        result = result + ('apply',)

    logger.info("notice_post view data : "+str(result))

    return render_template("/notice/notice_post.html", data=result)


