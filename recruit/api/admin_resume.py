#-*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.json import jsonify
from flask.globals import request
from recruit_base import dao
from recruit_base import admin_check

admin_resume_api=Blueprint("admin_resume_api", __name__)

@admin_resume_api.route("/get_resume_list", methods=["POST"])
@admin_check
def get_resume_list():
    param = request.values
    n_no = request.values['notice_no'] if 'notice_no' in request.values else ''
    search_val = request.values['search[value]'] if 'search[value]' in request.values else ''
    per_page = param.get('length')
        
    return_data = {}
    return_data['draw'] = int(param.get('draw'))
    
  
     
    #DB와 datatables libaray처리
    ##############################
     
    cursor = dao.get_conn().cursor()
    sql_str="select * from resume"
    if n_no != '':
        sql_str = sql_str + " where r_notice_no = %s" % (n_no)
    cursor.execute(sql_str)
    result = cursor.fetchall()
    cursor.close()
    ##############################
    return_data['recordsTotal'] = len(result)
    return_data['recordsFiltered'] = len(result)
    

    
    ##############################
    cursor = dao.get_conn().cursor()
    #sql_str="select resume.r_no, recruit_notice.n_title, resume.r_group1, resume.r_group2, resume.r_name, r_submit_time from recruit_notice join resume on resume.r_notice_no = recruit_notice.n_no"
    sql_str="select * from recruit_notice join resume on resume.r_notice_no = recruit_notice.n_no"
    
    if search_val.strip() != '':
        sql_str = sql_str + " and (n_title like '%"+str(search_val)+"%' or n_body like '%"+str(search_val)+"%' or n_sel1 like '%"+str(search_val)+"%' or n_sel2 like '%"+str(search_val)+"%' or r_selfintro1 like '%"+str(search_val)+"%' or r_selfintro2 like '%"+str(search_val)+"%' or r_selfintro3 like '%"+str(search_val)+"%' or r_name like '%"+str(search_val)+"%' or r_school_type like '%"+str(search_val)+"%' or r_school_name like '%"+str(search_val)+"%' or r_addr like '%"+str(search_val)+"%' )"
    
    if n_no == '':
        sql_str = sql_str + "  order by %s %s limit %s,%s" % (param.get('columns['+param.get('order[0][column]')+'][data]'), param.get('order[0][dir]'), param.get('start'), per_page)
    else:
        sql_str = sql_str + " and r_notice_no = %s order by %s %s limit %s,%s" % (n_no, param.get('columns['+param.get('order[0][column]')+'][data]'), param.get('order[0][dir]'), param.get('start'), per_page)
    
    cursor.execute(sql_str)
    col_names=cursor.description
    result = cursor.fetchall()
    cursor.close()
    ##############################
    
    post_list = []
    for row in result:
        tmp={}
        for col in range(0,len(col_names)):
            tmp[param.get('columns['+str(col)+'][data]')]=row[col]
        post_list.append(tmp)
        
        
    
    return_data['data'] = post_list
    return jsonify(return_data)

