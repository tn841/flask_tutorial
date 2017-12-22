#-*- coding:utf-8 -*-
'''
Created on 2017. 12. 19.

@author: tn841
'''
from flask.blueprints import Blueprint
from recruit_base import admin_check
from recruit_base import dao
from flask.globals import request, g
from flask.json import jsonify

admin_notice_api=Blueprint("admin_notice_api", __name__)

@admin_notice_api.route("/admin_notice_create", methods=["POST"])
@admin_check
def create_notice():
    
    n_title=request.values['n_title'] if 'n_title' in request.values else ''
    n_s_date=request.values['n_s_date'] if 'n_s_date' in request.values else ''
    n_e_date=request.values['n_e_date'] if 'n_e_date' in request.values else ''
    sel1=request.values['sel1'] if 'sel1' in request.values else ''
    sel2=request.values['sel2'] if 'sel2' in request.values else ''
    n_body=request.values['n_body'] if 'n_body' in request.values else ''
    
    data={}
    
    ################
    cursor = dao.get_conn().cursor()
    query_str="insert into recruit_notice (n_title, n_s_date, n_e_date, n_body, n_sel1, n_sel2) values('%s', '%s', '%s', '%s', '%s', '%s')" % (n_title.encode('utf-8'), n_s_date, n_e_date, n_body.encode('utf-8'), sel1.encode('utf-8'), sel2.encode('utf-8'))
    cursor.execute(query_str)
    g.conn.commit()
    a_row=cursor.rowcount
    cursor.close()
    ################
    
    if a_row == 1:
        data["RETURNCODE"] = 0
        data["RETURNMSG"] = "저장되었습니다."
    else:
        data["RETURNCODE"] = -1
        data["RETURNMSG"] = "서버 오류. 관리자에게 문의하세요."
    
    return jsonify(data)


@admin_notice_api.route("/admin_notice_remove", methods=["POST"])
@admin_check
def remove_notice():
    n_no=request.values['n_no'] if 'n_no' in request.values else ''
    
    data={}
    #######################
    cursor=dao.get_conn().cursor()
    query_str="delete from recruit_notice where n_no = %s" % (str(n_no))
    cursor.execute(query_str)
    g.conn.commit()
    a_row=cursor.rowcount
    cursor.close()
    #######################
    
    if a_row == 1:
        data["RETURNCODE"] = 0
        data["RETURNMSG"] = "삭제되었습니다."
    else:
        data["RETURNCODE"] = -1
        data["RETURNMSG"] = "서버 오류. 관리자에게 문의하세요."
        
    return jsonify(data)

@admin_notice_api.route("/admin_notice_modify", methods=["POST"])
@admin_check
def modify_notice():
    n_title=request.values['n_title'] if 'n_title' in request.values else ''
    n_s_date=request.values['n_s_date'] if 'n_s_date' in request.values else ''
    n_e_date=request.values['n_e_date'] if 'n_e_date' in request.values else ''
    sel1=request.values['sel1'] if 'sel1' in request.values else ''
    sel2=request.values['sel2'] if 'sel2' in request.values else ''
    n_body=request.values['n_body'] if 'n_body' in request.values else ''
    n_no=request.values['n_no'] if 'n_no' in request.values else ''
    
    data={}
    
    ################
    cursor = dao.get_conn().cursor()
    query_str="update recruit_notice set n_title='%s', n_s_date='%s', n_e_date='%s', n_body='%s', n_sel1='%s', n_sel2='%s' where n_no = %s " % (n_title.encode('utf-8'), n_s_date, n_e_date, n_body.encode('utf-8'), sel1.encode('utf-8'), sel2.encode('utf-8'), n_no)
    print query_str
    cursor.execute(query_str)
    g.conn.commit()
    a_row=cursor.rowcount
    cursor.close()
    ################
    
    print a_row
    
    if a_row == 1:
        data["RETURNCODE"] = 0
        data["RETURNMSG"] = "수정되었습니다."
    else:
        data["RETURNCODE"] = -1
        data["RETURNMSG"] = "서버 오류. 관리자에게 문의하세요."
    
    return jsonify(data)
    