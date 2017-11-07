#-*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.templating import render_template
from jinja2.exceptions import TemplateNotFound
from flask import abort

simple_page = Blueprint('simple_page', __name__, template_folder='templates', static_folder='static/page', static_url_path='/static_page')   #blueprint 객체 생성


@simple_page.route('/', defaults={'page':'index'})  #blueprint객체의 route데코레이터를 이용하여 URL과 view함수 매핑
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)  #templates/pages/ 하위에서 사용자가 요청한 page를 찾아 보여준다.
    except TemplateNotFound:
        abort(404)



