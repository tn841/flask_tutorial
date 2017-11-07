#-*- coding:utf-8 -*-

from flask import Flask
from simplecache import simple_cache

app =  Flask(__name__)
app.register_blueprint(simple_cache)

if __name__ == '__main__':
    app.run(port=2323, debug=True)