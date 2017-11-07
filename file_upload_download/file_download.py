#-*- coding:utf-8 -*-
import os

from flask import Blueprint, request, current_app, redirect
from flask.helpers import send_from_directory, send_file
from flask.templating import render_template

file_download = Blueprint('file_download', __name__)

@file_download.route('/')
def download_index():
    return render_template('/index.html')


@file_download.route('/download')
def download_file_func():
    download_file = request.args.get('filename')
    print "다운로드 파일명 : " + download_file
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], download_file)


@file_download.route('/download2')
def download_func2():
    file_name = request.args.get('filename')

    if file_name :
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)

        if not os.path.exists(file_path):
            from StringIO import StringIO
            strIO = StringIO()
            strIO.write("file not exitst")
            strIO.seek(0)

            file_path = strIO
            return  send_file(file_path, as_attachment=True, attachment_filename=file_path)
