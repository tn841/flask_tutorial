#-*- coding:utf-8 -*-
'''
Created on 2017. 12. 19.

@author: tn841
'''
from flask.blueprints import Blueprint
from flask.templating import render_template
from recruit_base import dao, admin_check
from mylogger import logger
from flask.globals import request

admin_view = Blueprint("admin_view", __name__)



@admin_view.route('/admin')
def admin_main():
    return render_template('/admin/admin_main.html')

@admin_view.route('/admin_notice')
@admin_view.route('/admin_notice/<page>')
@admin_check
def admin_notice(page=1):
    
   #################
    cursor = dao.get_conn().cursor()
    cursor.execute("select * from recruit_notice")
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
    
    
    
    #################
    cursor = dao.get_conn().cursor()
    query_str="select * from recruit_notice order by n_no DESC limit %s, %s" % (str(cur_page), str(per_page))
    cursor.execute(query_str)
    result=cursor.fetchall()
    cursor.close()
    #################

   

    logger.info("notice_board view data : " + str(result))
    return render_template('/admin/admin_notice.html', data=result, cur_page=cur_page, per_page=per_page, total_post=total_post, total_page=total_page)


@admin_view.route('/admin_notice_post')
@admin_check
def notice_post():
    notice_no = request.values['notice_no'] if 'notice_no' in request.values else ''
    
    #################
    cursor=dao.get_conn().cursor()
    query_str="select * from recruit_notice where n_no = %s" % (notice_no)
    cursor.execute(query_str)
    result=cursor.fetchone()
    col_names=cursor.description
    cursor.close()
    #################
    
    data={}
    
    for idx in range(0, len(result)):
        data[col_names[idx][0]]=result[idx]
        
    return render_template("/admin/admin_notice_modify.html", data=data)
    



@admin_view.route('/admin_resumeList')
@admin_check
def admin_resume_list():
    
    notice_data={}
    
    #######################
    cursor=dao.get_conn().cursor()
    query_str="select * from recruit_notice"
    cursor.execute(query_str)
    n_result=cursor.fetchall()
    n_cols=cursor.description
    cursor.close()
    #######################
    for row in range(0, len(n_result)):
        tmp={}
        for col_idx in range(0, len(n_cols)):
            tmp[n_cols[col_idx][0]] = n_result[row][col_idx]
        notice_data[row]=tmp
    
    
    #########column명 가져오기########
    cursor = dao.get_conn().cursor()
    sql_str="select * from recruit_notice join resume on resume.r_notice_no = recruit_notice.n_no"
    cursor.execute(sql_str)
    col_names=cursor.description
    cursor.close()
    ##############################
    names=[]
    for col in col_names:
        names.append(col[0])
    
    #보여질 column 리스트
    showing_col=['r_no', 'n_title', 'n_sel1', 'r_name', 'r_submit_time']
    
    return render_template('/admin/admin_resume.html', notice_data=notice_data, col_names=names, showing_col=showing_col)

@admin_view.route('/admin_userList')
@admin_check
def admin_user_list():
    return render_template('/admin/admin_users.html')




@admin_view.route("/admin_notice_form")
@admin_check
def admin_notice_form():
    return render_template("/admin/admin_notice_form.html")
    
    
    
