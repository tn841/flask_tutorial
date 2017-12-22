#-*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.templating import render_template

auth_view = Blueprint("auth_view", __name__)

@auth_view.route("/login")
def login_form():
    return render_template("auth/login.html")