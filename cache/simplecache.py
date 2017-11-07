#-*- coding:utf-8 -*-

from flask import Blueprint
from werkzeug.contrib.cache import SimpleCache
from datetime import datetime

simple_cache = Blueprint('simple_cache', __name__)
cache = SimpleCache()

@simple_cache.route('/get_item')
def simple_cache_view():
    rv = cache.get('my-item')
    if rv is None:
        rv = calculate_val()
        cache.set('my-item', rv, timeout=30)    #캐시 갱신 시간 30초로 설정
    return rv


def calculate_val():
    print '캐시값 계산, 시각 :',
    print datetime.now()
    return 'calc value test, ' + str(datetime.now())
