#-*- coding:utf-8 -*-

from flask import Flask, request, render_template
from wtforms import Form, BooleanField, PasswordField, validators, StringField, SubmitField

class RegistrationForm(Form):   #Form 클래스 상속
    username = StringField('username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Email(message='not in valid'), validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('confirm', message='passwords must match')])
    confirm = PasswordField('Repeat Password', [validators.DataRequired()])
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    submit = SubmitField('submit')


app =  Flask(__name__)

@app.route("/")
def index():
    return "WTForm lib tutorial"

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)   #위에서 정의한 Form클래스의 객체를 생성, 인자로 request.form을 넘겨준다.

    if request.method == 'POST':
        #등록 작업
        print request.form
        print form.errors
        return "registation complete"
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(port=2323, debug=True)