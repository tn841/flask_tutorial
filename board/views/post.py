#-*- coding: utf-8 -*-
from flask.blueprints import Blueprint
from flask.globals import request
from flask.templating import render_template

post_view = Blueprint("post_view", __name__)

@post_view.route("/post_form")
def post_form():
    board_name = request.values.get('board_name')
    return render_template("/post/write_post.html", board_name=board_name)