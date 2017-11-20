# -*- coding:utf-8 -*-
from datetime import datetime, timedelta

import jwt
from flask.app import Flask
from flask.globals import session, request
from flask.helpers import url_for, make_response
from flask.json import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'asdfasdf'
def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route("/")
def index():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
            # links is now a list of url, endpoint tuples
    print str(links)

    st = ''
    for item in links:
        st += "<a href="+item[0]+">"+item[1]+"</a><br>"

    return st

@app.route("/hash")
def hash():
    id = "111"
    pw = "111"

    hashed_pw = generate_password_hash(pw, salt_length=4)
    print hashed_pw
    print check_password_hash(hashed_pw, pw)

    return "pw"

@app.route("/jwt")
def jwt_func():

    json_token = {
        'UserKey' : 'userkey',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=30)
    }

    token = jwt.encode(json_token, 'secret_key', algorithm='HS256')
    print token
    access_token = token.decode('utf-8')


    session["access_token"] = access_token
    return str(access_token)

@app.route("/login")
@app.route("/login/<id>/<pw>")
def login(id=None, pw=None):
    print "id:%s, pw:%s" % (id, pw)
    payload = {
        'id' : id,
        'exp' : datetime.utcnow() + timedelta(seconds=300)
    }

    token = jwt.encode(payload, 'my_secret', algorithm='HS256')
    token = token.decode('utf-8')
    html = "<h1>jwt 테스트</h1><hr>"
    html += '<a href=/only_member>회원만</a>'
    res = make_response(html)
    res.set_cookie('my_token', value=token)

    return res

@app.route("/only_member")
def only_member_page():
    received_jwt = request.cookies['my_token']
    payload = jwt.decode(received_jwt,'my_secret')
    rv =  make_response(jsonify(payload))
    rv.headers['Content-Type']='application/json'
    return rv

if __name__ == '__main__':
    app.run(port=7778, debug=True)