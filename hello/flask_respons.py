#-*- coding:utf-8 -*-

import sys
from flask import Flask, Response

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

@app.route("/")
def index():
    resp = Response("사용자 응답 테스트")
    resp.headers.add('Name', 'Book')    #응답 헤더에 임의의 값 추가해보기
    return resp

if __name__ == '__main__':
    app.run(debug=True, port=2222)

