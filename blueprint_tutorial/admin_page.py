#-*- coding: utf-8 -*-
from flask.blueprints import Blueprint
from flask.templating import render_template
from jinja2.exceptions import TemplateNotFound
from werkzeug.exceptions import abort

admin_page = Blueprint('admin_page', __name__, template_folder='templates', url_prefix='/admin')    #admin_page객체로 매핑하는 url은 '/amdin'접두사가 붙게 된다.

@admin_page.route('/', defaults={'page':'index'})
@admin_page.route('/<page>')
def admin_index(page):
    try:
        return render_template('/admin/%s.html' % page)
    except TemplateNotFound:
        abort(404)