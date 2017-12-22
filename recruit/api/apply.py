#-*- coding:utf-8 -*-
from flask import jsonify, redirect
from flask.blueprints import Blueprint
from flask.globals import request, g
from flask.helpers import url_for, flash
from flask_login.utils import current_user, login_required

from recruit_base import try_except, dao, appliable_check
from mylogger import logger
from datetime import datetime

apply_api = Blueprint("apply_api", __name__)

@apply_api.route("/create_resume_action", methods=["POST"])
@login_required
@try_except
def create_resume():
    notice_no = request.values.get("notice_no") if "notice_no" in request.values else ''
    sel1 = request.values.get("sel1") if "sel1" in request.values else ''
    sel2 = request.values.get("sel2") if "sel2" in request.values else ''
    
    if not appliable_check(notice_no):
        flash("수정가능한 기간이 아닙니다.")
        return redirect(url_for("mypage_view.mypage"))
    
    data={}
    
    #######################
    cursor = dao.get_conn().cursor()
    query_str="select * from resume where r_notice_no = %s and r_writer_no = %s" % (notice_no, current_user.user_no)
    logger.info("create resume check query : "+query_str)
    cursor.execute(query_str)
    chk_r = cursor.fetchall()
    cursor.close()
    #######################
    if chk_r:
        data["RETURNCODE"] = -2
        data["RETURNMSG"] = "이미 작성한 지원서가 있습니다."

    else:
        if notice_no == '':
            data["RETURNCODE"] = -1
            data["RETURNMSG"] = "잘못된 접근입니다."
        else:
            c_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor = dao.get_conn().cursor()
            cursor.callproc("insert_r_resume", (notice_no, current_user.user_no, c_time, 0))
            cursor.execute("select @_insert_r_resume_3")
            result = cursor.fetchone()
            cursor.close()
            
            if int(result[0]) > 0 :
                data["sel1"] = sel1
                data["sel2"] = sel2
                data["notice_no"] = notice_no
                data["RETURNCODE"] = 0
                data["RETURNMSG"] = "success"
            else:
                data["RETURNCODE"] = -1
                data["RETURNMSG"] = "잘못된 접근입니다."

    return jsonify(data)

@apply_api.route("/step1_save_action", methods=["POST"])
@login_required
@try_except
def step1_save():
    logger.info("/step1_save_action params : "+str(request.values))
    sel1 = request.values.get('sel1') if 'sel1' in request.values else ''
    sel2 = request.values.get('sel2') if 'sel2' in request.values else ''
    notice_no = request.values.get("notice_no") if "notice_no" in request.values else ''
    
    if not appliable_check(notice_no):
        flash("수정가능한 기간이 아닙니다.")
        return redirect(url_for("mypage_view.mypage"))
    
    data = {}

    #####################
    cursor = dao.get_conn().cursor()
    query = "update resume set r_group1='%s', r_group2='%s' where r_writer_no=%d and r_notice_no=%d" % (sel1.encode('utf-8'), sel2.encode('utf-8'), int(current_user.user_no), int(notice_no))
    logger.info("query : "+query)
    cursor.execute(query)
    g.conn.commit()
    affected_row = cursor.rowcount
    #####################

    logger.info("affected_row : %s" % (affected_row))

    if affected_row == 1:
        data["notice_no"] = notice_no
        data["RETURNCODE"] = 0
        data["RETURNMSG"] = "저장되었습니다."
    else:
        data["RETURNCODE"] = -1
        data["RETURNMSG"] = "서버 오류. 관리자에게 문의하세요."

    return jsonify(data)


@apply_api.route("/step2_save_action", methods=["POST"])
@login_required
@try_except
def step2_save():
    logger.info("/step2_save_action params : "+str(request.values))
    name = request.values.get("name") if "name" in request.values else ""
    birth = request.values.get("birth") if "birth" in request.values else ""
    gender = request.values.get("gender") if "gender" in request.values else ""
    addr = request.values.get("addr") if "addr" in request.values else ""
    phone = request.values.get("phone") if "phone" in request.values else ""
    school_type = request.values.get("school_type") if "school_type" in request.values else ""
    school_name = request.values.get("school_name") if "school_name" in request.values else ""
    major = request.values.get("major") if "major" in request.values else ""
    grade = request.values.get("grade") if "grade" in request.values else ""
    career = request.values.get("career") if "career" in request.values else ""
    notice_no = request.values.get("notice_no") if "notice_no" in request.values else ''

    data={}
    
    if not appliable_check(notice_no):
        flash("수정가능한 기간이 아닙니다.")
        return redirect(url_for("mypage_view.mypage"))
    
    #####################
    cursor = dao.get_conn().cursor()
    query = "update resume set r_name='%s', r_birth='%s', r_gender='%s', r_addr='%s', r_phone='%s', r_school_type='%s', r_school_name='%s', r_major='%s', r_grade='%s', r_career='%s' " \
            "where r_writer_no=%d and r_notice_no=%d" % (name.encode('utf-8'), birth.encode('utf-8'), gender.encode('utf-8'), addr.encode('utf-8'), phone.encode('utf-8'), school_type.encode('utf-8'), school_name.encode('utf-8'), major.encode('utf-8'), grade.encode('utf-8'), career.encode('utf-8'), int(current_user.user_no), int(notice_no))
    logger.info("query : %s " % (query))
    cursor.execute(query)
    g.conn.commit()
    affected_row = cursor.rowcount
    #####################
    logger.info("affected_row : %s" % (affected_row))
    if affected_row == 1:
        data["notice_no"] = notice_no
        data["RETURNCODE"] = 0
        data["RETURNMSG"] = "저장되었습니다."
    else:
        data["RETURNCODE"] = -1
        data["RETURNMSG"] = "서버 오류. 관리자에게 문의하세요."

    return jsonify(data)



@apply_api.route("/step3_save_action", methods=["POST"])
@login_required
@try_except
def step3_save():
    logger.info("/step3_save_action params : "+str(request.values))
    list1_cert_name = request.values.get("list1_cert_name") if "list1_cert_name" in request.values else ""
    list1_cert_no = request.values.get("list1_cert_no") if "list1_cert_no" in request.values else ""
    list1_cert_date = request.values.get("list1_cert_date") if "list1_cert_date" in request.values else ""
    notice_no = request.values.get("notice_no") if "notice_no" in request.values else ''

    data={}
    
    if not appliable_check(notice_no):
        flash("수정가능한 기간이 아닙니다.")
        return redirect(url_for("mypage_view.mypage"))
    
    #####################
    cursor = dao.get_conn().cursor()
    query = "update resume set r_cert_name='%s', r_cert_no='%s', r_cert_date='%s' " \
            "where r_writer_no=%d and r_notice_no=%d" % (list1_cert_name.encode('utf-8'), list1_cert_no.encode('utf-8'), list1_cert_date.encode('utf-8'), int(current_user.user_no), int(notice_no))
    logger.info("query : %s " % (query))
    cursor.execute(query)
    g.conn.commit()
    affected_row = cursor.rowcount
    #####################
    logger.info("affected_row : %s" % (affected_row))
    if affected_row == 1:
        data["notice_no"] = notice_no
        data["RETURNCODE"] = 0
        data["RETURNMSG"] = "저장되었습니다."
    else:
        data["RETURNCODE"] = -1
        data["RETURNMSG"] = "서버 오류. 관리자에게 문의하세요."

    return jsonify(data)

@apply_api.route("/step4_save_action", methods=["POST"])
@login_required
@try_except
def step4_save():
    logger.info("/step4_save_action params : "+str(request.values))
    self_intro1 = request.values.get("self_intro1") if "self_intro1" in request.values else ""
    self_intro2 = request.values.get("self_intro2") if "self_intro2" in request.values else ""
    self_intro3 = request.values.get("self_intro3") if "self_intro3" in request.values else ""
    notice_no = request.values.get("notice_no") if "notice_no" in request.values else ''

    data={}
    
    if not appliable_check(notice_no):
        flash("수정가능한 기간이 아닙니다.")
        return redirect(url_for("mypage_view.mypage"))

    #####################
    cursor = dao.get_conn().cursor()
    query = "update resume set r_selfintro1='%s', r_selfintro2='%s', r_selfintro3='%s' " \
            "where r_writer_no=%d and r_notice_no=%d" % (self_intro1.encode('utf-8'), self_intro2.encode('utf-8'), self_intro3.encode('utf-8'), int(current_user.user_no), int(notice_no))
    logger.info("query : %s " % (query))
    print query
    cursor.execute(query)
    g.conn.commit()
    affected_row = cursor.rowcount
    #####################
    logger.info("affected_row : %s" % (affected_row))
    if affected_row == 1:
        data["notice_no"] = notice_no
        data["RETURNCODE"] = 0
        data["RETURNMSG"] = "저장되었습니다."
    else:
        data["RETURNCODE"] = -1
        data["RETURNMSG"] = "서버 오류. 관리자에게 문의하세요."

    return jsonify(data)

@apply_api.route("/step5_save_action", methods=["POST"])
@login_required
@try_except
def step5_save():
    logger.info("/step5_save_action params : "+str(request.values))
    submit_flag = request.values.get("submit_flag") if "submit_flag" in request.values else ""
    notice_no = request.values.get("notice_no") if "notice_no" in request.values else ''
    data={}
    
    if not appliable_check(notice_no):
        flash("수정가능한 기간이 아닙니다.")
        return redirect(url_for("mypage_view.mypage"))
    
    #####################
    cursor = dao.get_conn().cursor()
    cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = "update resume set r_submit=%d, r_submit_time='%s' where r_writer_no=%d and r_notice_no=%d" % (int(submit_flag), cur_time, int(current_user.user_no), int(notice_no))
    logger.info("query : %s " % (query))
    cursor.execute(query)
    g.conn.commit()
    affected_row = cursor.rowcount
    #####################
    logger.info("affected_row : %s" % (affected_row))
    if affected_row == 1:
        data["notice_no"] = notice_no
        data["RETURNCODE"] = 0
        data["RETURNMSG"] = "제출되었습니다."
    else:
        data["RETURNCODE"] = -1
        data["RETURNMSG"] = "서버 오류. 관리자에게 문의하세요."


    return jsonify(data)


@apply_api.route("/apply_remove_action", methods=["POST"])
@login_required
@try_except
def apply_remove():
    data={}
    logger.info("/apply_remove_action params : "+str(request.values))
    r_no = request.values.get("r_no") if "r_no" in request.values else ''
    r_writer_no = request.values.get("r_writer_no") if "r_writer_no" in request.values else ''


    if str(r_writer_no) == str(current_user.user_no):
        cursor = dao.get_conn().cursor()
        cursor.execute("delete from resume where r_no = %s" % (r_no))
        g.conn.commit()
        affected_row = cursor.rowcount
        if int(affected_row) == 1:
            data["RETURNCODE"] = 0
            data["RETURNMSG"] = "지원이 성공적으로 취소되었습니다."
        else:
            data["RETURNCODE"] = -1
            data["RETURNMSG"] = "취소실패. 관리자에게 문의하세요."
    else:
        data["RETURNCODE"] = -1
        data["RETURNMSG"] = "잘못된 접근입니다."

    return jsonify(data)