#-*- coding:utf-8 -*-
from flask.blueprints import Blueprint
from flask.globals import request, current_app
from flask.templating import render_template

import aes_cipher

auth_view = Blueprint("auth_view", __name__)

@auth_view.route("/login")
def login_form():
    print request.cookies
    enc_email = request.cookies.get('rmber') if 'rmber' in request.cookies else None
    email=''
    if enc_email:
        email = aes_cipher.decrypt(current_app.config['SECRET_KEY'], enc_email)


    return render_template("auth/login.html", email=email)