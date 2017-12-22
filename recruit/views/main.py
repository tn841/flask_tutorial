#-*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.globals import current_app, g
from flask.templating import render_template

from recruit_base import dao
from flask_login.utils import current_user
from datetime import datetime
from xhtml2pdf import pisa
from StringIO import StringIO
from flask.helpers import make_response

main_view = Blueprint("main_view", __name__)


@main_view.route("/pdf_test")
def pdf_test():
    
    source_html="<!DOCTYPE html><header><meta http-equiv='content-type' content='text/html; charset=utf-8'></header> <body style='boarder:2px'><h1 style='text-align:center'> 000 부문 지원 이력서 </h1> <hr> <h3>이력서 내용을 추가한다...</h3></body></html>"
    output="test.pdf"
    
    #파일로 저장
    result_file = open('./static/pdf/'+output, "w+b")
    
    #문자열로 저장
    result_str = StringIO()
    
    #변환
    #pisa_status = pisa.CreatePDF(source_html, dest=result_file)
    pisa_status = pisa.CreatePDF(source_html, result_str, encoding='utf-8')
    
    print pisa_status
    print result_str.getvalue()
    
    
    #파일스트림 닫기
    result_file.close()
    
    response = make_response(result_str.getvalue())
    response.headers["Content-Type"] = 'application/pdf'

    return response


@main_view.route("/")
def index():

    # from aes_cipher import decrypt
    # aes_cipher = "dalcoin1@3$5^7*9"
    # decrypted_number = decrypt(aes_cipher, "b/pGR+ybw8WJDdi2m5msgA==")

    return render_template("/index.html")


@main_view.route("/talent")
def right_people():
    return render_template("/side_menu/talent.html")


@main_view.route("/recruit_system")
def recruit_system():
    return render_template("/side_menu/recruit_system.html")

@main_view.route("/recruit_faq")
def recruit_faq():
    return render_template("/side_menu/recruit_faq.html")

@main_view.route("/recruit_pool")
def recruit_pool():
    data={
        'recruit_pool_no':0,
        'login_require':0
    }
    if not current_user.is_authenticated:
        data['login_require']=1
        
    return render_template("/side_menu/recruit_pool.html", data=data)

