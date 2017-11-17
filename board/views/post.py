#-*- coding: utf-8 -*-
from flask.blueprints import Blueprint
from flask.globals import request
from flask.templating import render_template

from db.database import DBManager

post_view = Blueprint("post_view", __name__)

@post_view.route("/post_form")
def post_form():
    board_name = request.values.get('board_name')
    return render_template("/post/write_post.html", board_name=board_name)


@post_view.route("/post_view/<p_id>")
def post_veiw_func(p_id=None):
    try:
        cursor = DBManager.conn.cursor()
        cursor.execute("select * from test_post where p_id = %s" % (p_id))
        result = cursor.fetchone()
        print str(result)
    except Exception as e:
        raise e

    return render_template("/post/view_post.html", post_data=result)

