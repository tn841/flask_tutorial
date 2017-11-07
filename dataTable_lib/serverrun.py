#-*- coding:utf-8 -*-

from flask import Flask, jsonify
from flask.helpers import make_response
from flask.templating import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/datatable.html')

@app.route("/server_processing", methods=['POST'])
def server_processing():
    data = dict()
    rv = make_response(jsonify(data))
    return rv

if __name__ == "__main__":
    app.run(port=2323, debug=True)