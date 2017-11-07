#-*- coding:utf-8 -*-

from flask import Flask
from flask.templating import render_template

from simple_page import simple_page
from admin_page import admin_page

app = Flask(__name__)
app.register_blueprint(simple_page, url_prefix='/pages')    #접두사는 blueprint객체를 만들때 붙여줄 수도 있고, 이처럼 Flask에 등록할때 설정 할 수 도 있다.
app.register_blueprint(admin_page)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print app.url_map
    with simple_page.open_resource('static/page/style.css') as f:
        print f.read()

    with app.open_resource('static/style.css') as f:
        print f.read()
    app.run(port=2323, debug=True)