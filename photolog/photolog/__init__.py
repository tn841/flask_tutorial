#-*- coding:utf-8 -*-

import os
from flask import Flask
from flask.templating import render_template


def print_settings(config):
    print "================================================"
    for key, val in config:
        print '%s = %s' % (key, val)
    print "================================================"

def page_not_found(error):
    return 'page not found', 404

def server_error(error):
    pass

def url_for_other_page(page):
    pass

def create_app(config_path='resource/config.json'):
    photolog_app = Flask(__name__)

    #config
    photolog_app.config.from_json(config_path)
    print_settings(photolog_app.config.iteritems()) #photolog_app의 모든 setting 확인

    #logger


    #DB
    from photolog.database import DBManager
    db_path = photolog_app.config['DB_URL']
    DBManager.init(db_path, True)
    DBManager.init_db()

    #View
    from controller import *

    from photolog_blueprint import photolog
    photolog_app.register_blueprint(photolog)


    #session


    #http error 헨들러
    #photolog_app.error_handler_spec[None][404] = page_not_found

    #템플릿 함수


    #secrte key
    photolog_app.secret_key = 'asdfasdf'
    return photolog_app

