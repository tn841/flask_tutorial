#-*- coding:utf-8 -*-

from flask import Flask, jsonify, render_template, request, make_response

app = Flask(__name__)

@app.route("/_add")
def add_num():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    dict = {}
    dict['result'] = a+b
    rv = make_response(jsonify(dict))
    rv.headers.add("Access-Control_allow_Origin", "*")  #동일 출처 원칙 회피
    return rv

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=2323, debug=True)
