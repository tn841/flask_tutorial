#-*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.globals import request
from flask.templating import render_template
from flask_login.utils import login_required, current_user
from mylogger import logger
from recruit_base import try_except, dao, appliable_check
from datetime import datetime
from flask.helpers import url_for, flash
from werkzeug.utils import redirect
from functools import wraps


apply_view = Blueprint("apply_view", __name__, url_prefix='/apply')


   
        

@apply_view.route("/step1")
@login_required
@try_except
def apply_step1():
    data = {}
    data['step'] = 1

    sel1 = request.values.get("sel1") if "sel1" in request.values else ''
    sel2 = request.values.get("sel2") if "sel2" in request.values else ''
    notice_no = request.values.get("notice_no") if "notice_no" in request.values else ''
    
    if not appliable_check(notice_no):
        flash("수정가능한 기간이 아닙니다.")
        return redirect(url_for("mypage_view.mypage"))

    data["sel1"] = sel1
    data["sel2"] = sel2

    ####################
    cursor = dao.get_conn().cursor()
    query_str="select r_group1, r_group2, r_notice_no from resume where r_writer_no = %s and r_notice_no = %s" % (current_user.user_no, notice_no) 
    cursor.execute(query_str)
    result = cursor.fetchall()
    col_names = cursor.description
    logger.info("apply_step1 query : "+query_str)
    if result:
        for idx in range(0, len(col_names)):
            data[col_names[idx][0]] = result[0][idx]
    ####################

    logger.info('apply_step1 view data : '+str(data))
    return render_template('apply/step1.html', data=data)

@apply_view.route("/step2")
@login_required
@try_except
def apply_step2():
    data = {}
    data['step'] = 2

    notice_no = request.values.get("notice_no") if "notice_no" in request.values else ''
    if not appliable_check(notice_no):
        flash("수정가능한 기간이 아닙니다.")
        return redirect(url_for("mypage_view.mypage"))
    ####################
    cursor = dao.get_conn().cursor()
    query_str="select r_name, r_birth, r_gender, r_addr, r_phone, r_school_type, r_school_name, r_major, r_grade, r_career, r_notice_no from resume where r_writer_no = %s and r_notice_no = %s" % (current_user.user_no, notice_no)
    cursor.execute(query_str)
    logger.info("apply_step2 query : "+query_str)
    result = cursor.fetchall()
    col_names = cursor.description

    if result:
        for idx in range(0, len(col_names)):
            data[col_names[idx][0]] = result[0][idx]
    ####################

    logger.info("apply_step2 view data : "+str(result))
    return render_template('apply/step2.html', data=data)

@apply_view.route("/step3")
@login_required
def apply_step3():
    data = {}
    data['step'] = 3

    notice_no = request.values.get("notice_no") if "notice_no" in request.values else ''
    if not appliable_check(notice_no):
        flash("수정가능한 기간이 아닙니다.")
        return redirect(url_for("mypage_view.mypage"))
    ####################
    cursor = dao.get_conn().cursor()
    query_str="select r_cert_name, r_cert_no, r_cert_date, r_notice_no from resume where r_writer_no = %s and r_notice_no = %s" % (current_user.user_no, notice_no) 
    cursor.execute(query_str)
    logger.info("apply_step3 query : "+query_str)
    result = cursor.fetchall()
    col_names = cursor.description

    if result:
        for idx in range(0, len(col_names)):
            data[col_names[idx][0]] = result[0][idx]
    ####################

    logger.info("apply_step3 view data : "+str(result))
    return render_template('apply/step3.html', data=data)

@apply_view.route("/step4")
@login_required
def apply_step4():
    data = {}
    data['step'] = 4

    notice_no = request.values.get("notice_no") if "notice_no" in request.values else ''
    if not appliable_check(notice_no):
        flash("수정가능한 기간이 아닙니다.")
        return redirect(url_for("mypage_view.mypage"))
    ####################
    cursor = dao.get_conn().cursor()
    query_str="select r_selfintro1, r_selfintro2, r_selfintro3, r_notice_no from resume where r_writer_no = %s and r_notice_no = %s" % (current_user.user_no, notice_no)
    logger.info("apply_step4 query : "+query_str)
    cursor.execute(query_str)
    result = cursor.fetchall()
    col_names = cursor.description

    if result:
        for idx in range(0, len(col_names)):
            data[col_names[idx][0]] = result[0][idx]
    ####################

    logger.info("apply_step4 view data : "+str(result))
    return render_template('apply/step4.html', data=data)

@apply_view.route("/step5")
@login_required
def apply_step5():
    data = {}
    data['step'] = 5

    notice_no = request.values.get("notice_no") if "notice_no" in request.values else ''

    ####################
    cursor = dao.get_conn().cursor()
    query_str="select * from resume where r_writer_no = %s and r_notice_no = %s" % (current_user.user_no, notice_no)
    logger.info("apply_step5 query : "+query_str)
    cursor.execute(query_str)
    result = cursor.fetchall()
    col_names = cursor.description

    if result:
        for idx in range(0, len(col_names)):
            data[col_names[idx][0]] = result[0][idx]
    ####################

    logger.info("apply_step5 view data : "+str(result))
    return render_template('apply/step5.html', data=data)