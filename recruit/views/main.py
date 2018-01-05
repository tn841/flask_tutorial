#-*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.globals import current_app, g, session
from flask.json import jsonify
from flask.templating import render_template

from recruit_base import dao
from flask_login.utils import current_user
from datetime import datetime


main_view = Blueprint("main_view", __name__)


@main_view.route("/")
def index():
    return render_template("/index.html")

@main_view.route("/sessoin_check", methods=["POST"])
def session_expire_check():
    print session.clear
    return jsonify({'data':'ok'})

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

