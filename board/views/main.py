# -*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.globals import request, current_app
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect

main_view = Blueprint('main_view', __name__, template_folder='templates')

@main_view.route('/', methods=['GET'])
def index():
    return redirect(url_for('.main'))

@main_view.route('/main', methods=['GET'])
def main():
    return render_template('main.html', config = current_app.config)

@main_view.route('/test', methods=['POST'])
def test_view():
    return str(request.values.copy())

@main_view.route('/test', methods=['GET'])
def test_view2():
    return str(request.values.copy())