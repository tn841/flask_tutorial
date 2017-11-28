#-*- coding: utf-8 -*-
from flask.blueprints import Blueprint
from flask.globals import request
from flask.templating import render_template

from db.database import DBManager

from board_base import db_exception, db

post_view = Blueprint("post_view", __name__)

@post_view.route("/post_form")
def post_form():
    board_name = request.values.get('board_name')
    return render_template("/post/write_post.html", board_name=board_name)


@post_view.route("/post_view/<p_id>")
@db_exception
def post_veiw_func(p_id=None):

    cursor = db.get_conn().cursor()
    cursor.execute("select * from test_post where p_id = %s" % (p_id))
    result = cursor.fetchone()
    print str(result)

    return render_template("/post/view_post.html", post_data=result)

