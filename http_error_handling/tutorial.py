#-*- coding:utf-8 -*-

from flask import Flask, abort

app = Flask(__name__)

@app.route("/")
def index():
    return "http error handling page"

@app.route("/404")
def page_404():
    abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return "요청하신 페이지를 찾을 수 없습니다."


if __name__ == "__main__":
    app.run(port=2323, debug=True)
