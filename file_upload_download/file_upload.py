#-*- coding:utf-8 -*-
import os
import sys
from flask.blueprints import Blueprint
from flask import request, current_app
from flask.helpers import flash
from flask.templating import render_template
from werkzeug.utils import secure_filename
from flask import redirect
from wtforms import Form, FileField, validators


#파일 업로드 기능을 담당하는 blueprint객체 생성
file_upload = Blueprint('file_upload_download', __name__)

#파일 업로드 form을 생성하는 클래스 정의
class File_upload_form(Form):
    file_field = FileField('File', [validators.required])   #valiator에 정규식을 이용하여 확장자를 제한하거나 특수문자등을 제한할 수 있다.


@file_upload.route('/upload_form')
def file_upload_form():
    upload_form = File_upload_form(request.form)    #위에서 정의한 File_upload_form클래스의 객체를 생성한다, 인자로 request.form을 넘겨줘야한다.
    return render_template('/form.html', form=upload_form)


@file_upload.route('/upload_action', methods=['POST'])
def upload_action_func():
    if request.method == 'POST':
        if 'file_field' not in request.files:
            flash('파일 form이 없습니다..')
            return redirect('/upload_form')
        file =  request.files['file_field'] #werkzeug모듈의 FileStorage클래스 인스턴스로 반환된 file객체
        if file.filename == '':
            flash('파일을 선택하세요 ')
            return redirect('/upload_form')
        if file:
            filename = secure_filename(file.filename)  # secure_filename()메소드로 사용자 임의의 값 방지, 영어만 지원함, 사용자 지정 함수를 만드는 것이 보안상 좋음
            print '업로드 파일명 : ' + filename
            if '.' not in filename or filename.rsplit('.',1)[1] not in current_app.config['ALLOWED_EXTENSIONS']:
                flash('extensions denied')
                return redirect('/upload_form')
            print '업로드 폴더 : ' + current_app.config['UPLOAD_FOLDER'] #flask config값을 가져오기위해 current_app객체 이용
            print 'secure_filename(filename) : ' + secure_filename(filename)
            print '최종 업로드 경로 : ' + os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))  #file객체의 save메소드를 이용하여 임시 저장된 파일을 지정된 폴더로 복사
            flash(filename+" uploading completed.")
            return redirect('/upload_form')

