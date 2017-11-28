# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
from time import time

import jwt
from flask import Flask
from flask.globals import request, session
from flask.helpers import make_response
from flask.json import jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = '11'



@app.route("/")
def index():


    payload = {
        "iss" : time(),
        "exp" : datetime.utcnow() + timedelta(seconds=60),
        "user_id" : "aownw22",
        "auth_level" : 3
    }
    jwtoken = jwt.encode(payload, "1234")
    html = "<a href='/aa'>요청</a>"
    for item in app.config:
        html += "<pre>"+item+":"+str(app.config.get(item))+"</pre>"
    html += "<script>console.log(document.cookie)</script>"

    res = make_response(html)
    #res.set_cookie('jwt', value=jwtoken)
    session['jwt'] = jwtoken
    return res


@app.route("/aa")
def aa_view():
    cookie_data = request.cookies

    auth = request.authorization
    print str(auth)
    html = str(cookie_data)
    html += str(auth)

    res  = make_response(html)
    for item in cookie_data:
        res.set_cookie(item, '', expires=0)

    return res


@app.route("/2")
def main2():
    payload = {
        "iss": time(),
        "exp": datetime.utcnow() + timedelta(seconds=60),
        "user_id": "aownw22",
        "auth_level": 3
    }
    jwtoken = jwt.encode(payload, "4321")
    html = "<a href='/aa'>요청</a>"
    html += jwtoken
    rv = make_response(html)

    rv.headers['Authorization'] = "Bearer %s" % (jwtoken)
    return rv

if __name__ == '__main__':
    app.run(port=7788, debug=True)


