#-*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.templating import render_template
from flask_login.utils import current_user, login_required
from mylogger import logger
from recruit_base import dao
from datetime import datetime

mypage_view = Blueprint("mypage_view", __name__)

@mypage_view.route("/mypage")
@login_required
def mypage():

    ##########################
    cursor = dao.get_conn().cursor()
    join_query = "select * from resume join recruit_notice on resume.r_notice_no = recruit_notice.n_no and resume.r_writer_no=%s" % (current_user.user_no)
    cursor.execute(join_query)
    result = cursor.fetchall()
    col_names = cursor.description
    ##########################
    
 
    data={}
    if result:
        for row in range(0, len(result)):
            temp={}
            for idx in range(0, len(col_names)):
                temp[col_names[idx][0]] = result[row][idx]
            temp['expire_chk'] = 0
            
            if result[row][29] < datetime.now():
                temp['expire_chk'] = 1
            data[row] = temp

    
    logger.info("mypage view data : "+str(data))    
    return render_template("/mypage/mypage.html", data=data)


