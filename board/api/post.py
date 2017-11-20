# -*- coding: utf-8 -*-
import json
from datetime import datetime

from flask.blueprints import Blueprint
from flask.globals import request, current_app

from db.database import DBManager
from flask.helpers import flash, url_for, make_response
from flask.json import jsonify
from flask.templating import render_template
from flask_login.utils import login_required, current_user
from mylogger import logger
from werkzeug.utils import redirect

post_api = Blueprint("post_api", __name__)

@post_api.route("/insert_post_action", methods=['POST'])
def insert_post():

    data = request.values
    logger.info("form data : " + str(data))
    p_title = data.get('p_title') if data.get('p_title') else None
    p_body = data.get('p_body') if data.get('p_title') else None
    p_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    p_writer = data.get('p_writer') if data.get('p_writer') else None
    b_id = None
    if data.get('b_type') == 'common_board/':
        b_id = 1
    elif data.get('b_type') == 'member_board/':
        b_id = 2

    logger.info("post insert : "+str(p_title)+", "+str(p_body)+", "+str(p_date)+", "+str(p_writer)+", "+str(b_id))
    try:
        cursor = DBManager.conn.cursor()
        cursor.callproc('insert_post',(p_title, p_body, p_date, p_writer, b_id, 0))
        cursor.execute('select @_insert_post_5')
        result = cursor.fetchone()
        logger.info("post insert result : "+str(result[0]))
        if result[0] == 0:
            flash("글이 등록 되었습니다.")
            if b_id == 1:
                return redirect(url_for("board_view.common_board"))
            elif b_id == 2:
                return redirect(url_for("board_view.member_board"))
        else:
            flash("글 등록과정에서 오류가 발생하였습니다.")
            return redirect(url_for("post_view.post_form"))
    except Exception as e:
        logger.info(str(e))
    finally:
        cursor.close()


@post_api.route("/modify_post_action", methods=['POST'])
def modify_post_action():
    data = request.values
    try:
        cursor = DBManager.conn.cursor()
        sql = "update test_post set p_title='%s', p_body='%s' where p_id = %s" % (str(data.get('p_title')), data.get('p_body'), str(data.get('p_id')).replace('/',''))
        print sql
        rr = cursor.execute(sql)
        print "수정결과 :"+str(rr)
        cursor.close()
        flash(str(data.get('p_id'))+"번 글이 수정되었습니다.")
        return redirect(url_for("board_view.member_board"))
    except Exception as e:
        raise e



@post_api.route("/get_post_list", methods=['POST'])
def get_common_post_list():
    param = request.values
    per_page = param.get('length')

    return_data = {}
    return_data['draw'] = int(param.get('draw'))
    #DB와 datatables libaray처리
    try:
        cursor = DBManager.conn.cursor()
        cursor.callproc("get_total_post_cnt", (1,))
        result = cursor.fetchone()
        cursor.close()
        return_data['recordsTotal'] = result[0]
        return_data['recordsFiltered'] = result[0]

        cursor = DBManager.conn.cursor()
        #cursor.callproc("select_post_list", (param.get('start'), per_page, 1))

        sql = "select p_id, p_title, p_body, p_date, p_writer, board_id from test_post where board_id = %s order by %s %s limit %s,%s" % ("1", param.get('columns['+param.get('order[0][column]')+'][data]'), param.get('order[0][dir]'), param.get('start'), per_page)
        print param.get('columns['+param.get('order[0][column]')+'][data]')
        print sql
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        post_list = []
        for row in result:
            post_list.append({
                param.get('columns[0][data]') : row[0],
                param.get('columns[1][data]') : row[1],
                param.get('columns[2][data]') : row[3],
                param.get('columns[3][data]') : row[4]
            })
        print str(post_list)
        return_data['data'] = post_list

        return make_response(jsonify(return_data))
    except Exception as e:
        print str(e)
        raise e


@post_api.route("/get_m_post_list", methods=['POST'])
def get_member_post_list():
    param = request.values
    per_page = param.get('length')

    return_data = {}
    return_data['draw'] = int(param.get('draw'))
    #DB와 datatables libaray처리
    try:
        cursor = DBManager.conn.cursor()
        cursor.callproc("get_total_post_cnt", (2,))
        result = cursor.fetchone()
        cursor.close()
        return_data['recordsTotal'] = result[0]
        return_data['recordsFiltered'] = result[0]

        cursor = DBManager.conn.cursor()
        #cursor.callproc("select_post_list", (param.get('start'), per_page, 1))

        sql = "select p_id, p_title, p_body, p_date, p_writer, board_id from test_post where board_id = %s order by %s %s limit %s,%s" % ("2", param.get('columns['+param.get('order[0][column]')+'][data]'), param.get('order[0][dir]'), param.get('start'), per_page)
        print param.get('columns['+param.get('order[0][column]')+'][data]')
        print sql
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        post_list = []
        for row in result:
            post_list.append({
                param.get('columns[0][data]') : row[0],
                param.get('columns[1][data]') : row[1],
                param.get('columns[2][data]') : row[3],
                param.get('columns[3][data]') : row[4]
            })
        print str(post_list)
        return_data['data'] = post_list

        return make_response(jsonify(return_data))
    except Exception as e:
        print str(e)
        raise e


@post_api.route("/remove_post", methods=["get"])
@login_required
def remove_post():
    p_id = request.values.get("p_id")
    #삭제전에 삭제하려는 글이 현재 로그인한 사용자가 작성한 글인지 검증 필요
    try:
        cursor = DBManager.conn.cursor()
        sql = "select p_date, board_id from test_post where p_id = %s" % (p_id)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close
        if result[0].replace('/','') == current_user.user_id:
            print "작성자가 삭제를 시도함, board_id:"+str(result[1])
            sql = "delete from test_post where p_id = %s" % (p_id)
            cursor = DBManager.conn.cursor()
            result2 = cursor.execute(sql)
            cursor.close()
            print "삭제 결과 : "+str(result2)
            if result[1] == 1:
                flash(p_id+"번 게시글이 삭제되었습니다.")
                return redirect(url_for("board_view.common_board"))
            elif result[1] == 2:
                flash(p_id+"번 게시글이 삭제되었습니다.")
                return redirect(url_for("board_view.member_board"))
        else:
            flash("잘못된 접근 입니다.")
            return redirect(url_for("main_view.index"))
    except Exception as e:
        raise  e


@post_api.route("/modify_post", methods=["get"])
@login_required
def modify_post():
    p_id = request.values.get("p_id")
    # 수정하려는 글이 현재 로그인한 사용자가 작성한 글인지 검증 필요
    try:
        data={}
        cursor = DBManager.conn.cursor()
        sql = "select * from test_post where p_id = %s" % (p_id)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close

        print str(result)
        data['title'] = result[1]
        data['body'] = result[2]
        data['p_id'] = result[0]

        if str(result[3]).replace('/','') == current_user.user_id:
            print "작성자가 수정을 시도함, board_id:"+str(result[1])
            #flash(p_id + "번 게시글이 수정 되었습니다.")
            if result[5] == 1:
                return render_template('/post/modify_post.html', data=data, board_name="common_board")
            elif result[5] == 2:
                return render_template('/post/modify_post.html', data=data, board_name="member_board")
        else:
            flash("잘못된 접근 입니다.")
            return redirect(url_for("main_view.index"))
    except Exception as e:
        raise  e
