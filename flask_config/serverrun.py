#-*- coding:utf-8 -*-

from flask import Flask

app = Flask(__name__)

#Builtin 방식으로 config 설정
app.config['DEBUG'] = True
app.debug = True
app.config.update(
    DEBUG=True,
    SECRET_KEY = '123123'
)

#파일에서 config 설정하기
app.config.from_object('application.configs')   #config 클래스 활용
app.config.from_envvar('config_file_path')      #config 파일 활용
app.config.from_json('config_json_file_path', silent=True)   #json파일 활용, silent 속성으로 config에러를 무시할 수있음..


#Instance Folders
'''
    Flask 어플리케이션을 생성할때, instance 폴더를 명시적으로 알려주거나 Flask가 자동으로 instance 폴더를 찾게할 수 있다.
    instance폴더를 명시하지 않을경우 다음 위치에서 instance폴더를 찾는다.
        /app.py
        /instance
        
        /app
            /__init__.py
        /instance
'''
    #명시적으로 알려주기
app = Flask(__name__, instance_path='/path/path2/folder') #절대경로로 적어야한다.

    #auto detecting
app = Flask(__name__, instance_relative_config=True)


if __name__ == '__main__':
    app.run(port=2323, debug=True)