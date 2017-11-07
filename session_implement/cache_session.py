# -*- coding: utf-8 -*-
"""
    photolog.cache_session
    ~~~~~~~~~~~~~~~~~~~~~~

    Cache를 이용한 서버 세션 모듈.
    1. 로컬 어플리케이션 서버의 메모리를 이용하는 SimpleCache 버전과
    2. RedisCache를 이용해서 가용성을 보장하는 버전 두가지를 제공함.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from datetime import timedelta
from uuid import uuid4
from werkzeug.contrib.cache import NullCache, SimpleCache, RedisCache
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin


class CacheSession(CallbackDict, SessionMixin):
    '''
    - dict의 변화를 감시하여 콜백함수를 호출하는 CallbackDict클래스와 세션의 속성을 사용하기위해 SessionMinxin클래스를 상속
    - 이 클래스는 open_session() 메서드에서 결과값으로 반환하는 클래스이다.
    '''
    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
            
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class CacheSessionInterface(SessionInterface):
    '''
    - open_session(), save_session() 메서드를 이용해 오버라이드 한다.
    '''
    session_class = CacheSession

    def __init__(self, cache=None, prefix='cache_session:'):
        if cache is None:
            cache = NullCache()
        self.cache = cache
        self.prefix = prefix

    def generate_sid(self):
        return str(uuid4())

    def get_cache_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)

    def open_session(self, app, request):   #요청이 들어올때 seesion을 반환하는 것이 open_session()메소드의 최종 목적
        print 'open_session()',
        sid = request.cookies.get(app.session_cookie_name)

        if not sid: #sid가 없다면
            sid = self.generate_sid()   #sid 생성
            print 'sid없음, 새로운 session생성, ' + str(sid)
            return self.session_class(sid=sid, new=True)
           
        val = self.cache.get(self.prefix + sid)
        print 'sid있음 : ' + str(sid) + ', val : ' + str(val) + ", ",
        if val is not None:
            print 'val 있음, 그 값으로 세션을 만듦'
            return self.session_class(val, sid=sid)
        print 'val 없음, 값이 없는 세션을 생성'
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        print 'save_session()  domain : '+str(domain)
        if not session:
            self.cache.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name, domain=domain)
            return

        cache_exp = self.get_cache_expiration_time(app, session)
        
        val = dict(session)
        self.cache.set(self.prefix + session.sid, val, 
                       int(cache_exp.total_seconds()))
        
        response.set_cookie(app.session_cookie_name, 
                            session.sid,
                            httponly=True,
                            domain=domain)
         
    
class SimpleCacheSessionInterface(CacheSessionInterface):

    def __init__(self):
        
        CacheSessionInterface.__init__(self, 
                                       cache=SimpleCache(), 
                                       prefix='simple_cache_session:')

#
# class RedisCacheSessionInterface(CacheSessionInterface):
#
#     def __init__(self,
#                  host='localhost',
#                  port=6379):
#
#         cache = RedisCache(host=host, port=port)
#         CacheSessionInterface.__init__(self,
#                                        cache,
#                                        prefix='redis_cache_session:')

