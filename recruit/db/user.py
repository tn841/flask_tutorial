# -*- coding:utf-8 -*-

'''
    - flask-login 모듈을 활용하기 위해 User클래스는 몇가지 필수 속성과 메소드를 구현해야 한다.
    - UserMixin 클래스를 상속받아 구현할 수도 있다.
'''

class User:
    def __init__(self, email, auth=False, name='', no=''):
        self.user_email = email
        self.authenticated = auth
        self.user_name = name
        self.user_no = no

    def __repr__(self):
        r = {
            'user_email':self.user_email,
            'authenticated':self.authenticated,
            'user_name':self.user_name,
            'user_no':self.user_no
        }
        return str(r)

    def is_authenticated(self):
        '''user객체가 인증되었다면 True를 반환'''
        return self.authenticated

    def is_active(self):
        '''특정 계정의 활성화 여부, inactive 계정의 경우 로그인이 되지 않도록 설정할 수 있다.'''
        return True

    def is_anonymous(self):
        '''익명의 사용자로 로그인 할 때만 True반환'''
        return False

    def get_id(self):
        '''
        - 사용자의 ID를 unicode로 반환
        - user_loader 콜백 메소드에서 사용자 ID를 얻을 때 사용할 수도 있다.
        '''
        return self.user_email

