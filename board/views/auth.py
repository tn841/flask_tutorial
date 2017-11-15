# -*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.templating import render_template
from wtforms import validators
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField
from wtforms.form import Form

auth_view = Blueprint('auth_view', __name__)

@auth_view.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html')


