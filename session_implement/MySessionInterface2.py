#-*- coding:utf-8 -*-
'''
    - 어떤 이유에서 인지 MySeesionInterface가 제대로 동작하지 않아 MySessionInterface2 재 구현,,
        => run.py에서 import할때, 최종 구현 클래스를 import해야하는데 MySessionInterface클래스를 import한 것이 문제 였음..
'''
from uuid import uuid4

from datetime import timedelta
from flask.sessions import SessionMixin, SessionInterface
from werkzeug.contrib.cache import NullCache, SimpleCache
from werkzeug.datastructures import CallbackDict


class MySession(CallbackDict, SessionMixin):
    '''
    - 실제 데이터를 가지는 session객체를 정의하는 클래스
    - 요구조건  1. Dict형 클래스인 CallbackDict를 상속받는다.
                2. SessionMixin클래스를 상속 받는다.
    '''
    def __init__(self, initial = None, sid = None, new=False):
        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.modified = False
        self.new = new

class MySessionInterface(SessionInterface):
    '''
    - http요청이 들어올때 실행되는 open_session()메소드를 구현해야한다.
    - http응답시 필요한 save_session()메소드를 구현해야한다.
    '''

    session_class = MySession

    def __init__(self, cache=None, prefix='cache_session'):
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


    def open_session(self, app, request):
        print 'open_session()'
        sid = request.cookies.get(app.session_cookie_name)

        if not sid:
            sid = self.generate_sid()
            print 'sid없음, 새로운 session생성, ' + str(sid)
            return self.session_class(sid=sid, new=True)

        val = self.cache.get(self.prefix + sid) #캐시에서 특정 sid를 key로하는 value를 가져온다.
        print 'sid있음 : ' + str(sid) + ', val : ' + str(val) + ", ",
        if val is not None:
            print 'val 있음, 그 값으로 세션을 만듦'
            return self.session_class(initial=val, sid=sid)
        print 'val 없음, 값이 없는 세션을 생성'
        return self.session_class(sid=sid, new=True)



    def save_session(self, app, session, response):
        print 'save_session()'

        domain = self.get_cookie_domain(app)

        #???????????
        if not session:
            self.cache.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name, domain=domain)
            return
        cache_exp = self.get_cache_expiration_time(app, session)

        val = dict(session)
        self.cache.set(self.prefix + session.sid, val, int(cache_exp.total_seconds()))

        response.set_cookie(app.session_cookie_name, session.sid, httponly=True, domain=domain)


class SimpleCacheSessioninterface(MySessionInterface):
    def __init__(self):
        MySessionInterface.__init__(self, SimpleCache(), prefix='my_cache_session')















