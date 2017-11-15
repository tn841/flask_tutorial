# -*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.templating import render_template
from flask_login.utils import login_required

board_view = Blueprint("board_view", __name__)

@board_view.route("/common_board")
def common_board():
    return render_template("/board/common_board.html")

@board_view.route("/member_board")
@login_required
def member_board():
    return render_template("/board/member_board.html")