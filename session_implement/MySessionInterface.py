#-*- coding:utf-8 -*-

from uuid import uuid4

from datetime import timedelta, datetime
from flask.sessions import SessionMixin, SessionInterface
from werkzeug.datastructures import CallbackDict
from werkzeug.contrib.cache import SimpleCache, NullCache


class MySession(CallbackDict, SessionMixin):
    '''
        - 실제 session객체를 저장하는 MySession 클래스
        - dict형 클래스와, SessionMixin클래스를 상속 받아야한다.
        - dict형 클래스는 werkzeug의 CallbackDict클래스를 사용
    '''
    def __init__(self, initial=None, sid=None, new=False):
        '''
        :param initial:초기값
        :param sid: 세션id
        :param new: 새로 생성되었는지 여부
        '''
        def on_update(self):    #내포 함수
            self.modified = True
            print 'on_update()'

        CallbackDict.__init__(self, initial, on_update)   #값이 변하면 CallbackDict가 동작한다.
        self.sid = sid
        self.new = new
        self.modified = False





class MySessionInterface(SessionInterface):
    '''
        - SessionInterface는 Flask가 사용하는 기본 session을 대체하는 방법을 제공한다.
        - open_session()과 save_session() 메소드를 구현해야한다.
        - open_session()에의해 반환되는 session객체는
          SessionMixin이 제공하는 속성과 메소드들을 추가한 dictionary클래스를 제공해야한다.
    '''
    session_class = MySession   #실제 session 객체를 저장하는 객체

    def __init__(self, cache=None, prefix='mysession:'):
        if cache is None:
            cache = NullCache()
        self.cache = cache
        self.prefix = prefix

    def generate_sid(self):
        '''
            - 고유의 sid를 생성하는 메소드
        '''
        sid = str(uuid4())
        print 'generate_sid('+sid+')'
        return sid

    def open_session(self, app, request):
        '''
            - http세션을 열때 호출되는 open_session()메소드

        :param app: flask app객체
        :param request: http request객체
        :return: session_class객체, 실제 session정보를 저장하는 객체
        '''
        print 'open_session()  app.session_cookie_name : '+app.session_cookie_name,
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            print 'sid 없음->새로운 session 생성'
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        val = self.cache.get(self.prefix + sid)
        print 'sid 있음 : ' + str(sid) + ', val : ' + str(val) + ", ",
        if val is not None:
            print 'val 있음, 그 값으로 세션을 만듦'
            return self.session_class(val, sid=sid)
        print 'val 없음, 값이 없는 세션을 생성'
        return self.session_class(sid=sid, new=True)


    def save_session(self, app, session, response):
        '''
            - http세션을 저장할 때(http요청이 완료될 때) 호출되는 save_session()메소드

        :param app:
        :param session:
        :param response:
        :return:
        '''
        print 'save_session()',
        domain = self.get_cookie_domain(app)    #세션이 동작하는 도메인을 가져온다.
        if not session:                                     #세션에 값이 없다면
            print 'session에 값이 없음, 캐시에서 해당 sid를 갖는 세션을 삭제한다.  ',
            self.cache.delete(self.prefix + session.sid)    #캐시에서 해당 세션을 삭제한다.
            if session.modified:                            #세션에 값도 없고 세션이 수정되었다면
                print '  또한 session에 값이 없으면서 세션이 수정되었다면 로그아웃을 수행하는 것. '
                response.delete_cookie(app.session_cookie_name, domain=domain)  #쿠기를 삭제한다. (로그아웃의 경우)
            return

        #session 만료시간 계산
        cache_expire = timedelta(days=1)    # 1일로 설정
        if session.permanent:        #app.config에서 지정한 만료시간이 있다면 그걸로 설정
            cache_expire = app.permanent_session_lifetime
        print 'cache_expire : ' + str(cache_expire.total_seconds())
        val = dict(session)
        print 'dict(session) : ' + str(val.copy()),
        self.cache.set(self.prefix + session.sid, val, int(cache_expire.total_seconds()))

        response.set_cookie(app.session_cookie_name, session.sid, httponly=True, domain=domain)

class MySimpleCacheSessionInterface(MySessionInterface):
    '''
        - 실제 데이터를 저장하는 cache 종류에 따라 구현체를 나누기위해 정의한 클래스
        - 이 클래스에서는 SimpleCache를 이용한다.
    '''
    def __init__(self):
        MySessionInterface.__init__(self, cache=SimpleCache(), prefix='simple_cache_session:')
