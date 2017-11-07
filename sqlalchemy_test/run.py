#-*- coding:utf-8 -*-

import sys
from flask import Flask, logging
from database import init_db, db_session
from models import User

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

@app.teardown_appcontext
def tesrdown_session(exception=None):
    print "앱 종료시 db연결 해제"
    db_session.remove()

@app.route("/")
def index():
    return "flask - mysql 연동"

@app.route("/create_user/<name>/<email>")
def create_users(name, email):
    new_user = User(name, email)
    ff = db_session.add(new_user)
    db_session.commit()
    return name + ", " + email + " 유저 생성 완료" + str(ff)

@app.route("/select_all_user")
def all_user():
    print str(User.query.all())
    return ''

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=2323)