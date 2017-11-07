#-*- coding:utf-8 -*-
import sys
from flask import Flask
from file_upload import file_upload
from file_download import file_download

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.secret_key = 'aa'
app.register_blueprint(file_upload)
app.register_blueprint(file_download)

app.config['ALLOWED_EXTENSIONS'] = set(['txt'])
app.config['UPLOAD_FOLDER'] = './uploads'

@app.route("/")
def index():
    return "<h1>file_upload_download tutorial</h1>"

if __name__ == '__main__':
    print app.url_map
    app.run(port=2323, debug=True)