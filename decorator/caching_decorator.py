#-*- coding:utf-8 -*-

from flask import Flask, request
from functools import wraps
from werkzeug.contrib.cache import RedisCache

app = Flask(__name__)

cache = RedisCache()


'''
- 사용자가 요청한 URL주소를 유효기간이 5분인 cache key로 만드는 데코레이터
- DB 접속을 매번하지 않고 timeout시간동안 메모리에 캐시된 데이터를 사용한다.
- 특정 페이지에 요청이 많을 때 사용. 
'''
def cached(timeout=5 * 60, key='view/%s'):  #기본 timeout시간과 key값을 설정
    def decorator(f):
        @wraps(f)
        def deco_func(*args, **kwargs):
            cache_key = key%request.path
            rv = cache.get(cache_key)
            if rv is None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return deco_func
    return decorator


@app.route("/")
def index():
    return "cache decorator index page"


@app.route("/cached_page")
@cached(timeout=10*60, key="/cached/%s")
def cached_view():
    return "this page was cached."





if __name__ == "__main__":
    app.run(debug=True, port=2323)