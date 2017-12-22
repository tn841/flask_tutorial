#-*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.templating import render_template

register_view = Blueprint("register_view", __name__)

@register_view.route("/register")
def register_form():
    return render_template("register.html")