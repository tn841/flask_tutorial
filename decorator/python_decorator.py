#-*- coding:utf-8 -*-

import datetime
from functools import wraps

def datetime_deco(func):
    def decorated():
        print datetime.datetime.now()
        func()
        print datetime.datetime.now()
        print ""
    return decorated()

class Datetime_deco2:
    def __init__(self, f):
        self.func = f

    def __call__(self, *args, **kwargs):
        print datetime.datetime.now()
        self.func(*args, **kwargs)
        print datetime.datetime.now()



@datetime_deco
def func1():
    print "func1()"


@datetime_deco
def func1():
    print "func2()"


@datetime_deco
def func1():
    print "func3()"



'''
@wraps 데코레이터 기능??
'''
def without_wraps(f):
    def __wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return __wrapper


def with_wraps(f):
    @wraps(f)
    def __wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return __wrapper


@without_wraps
def my_func():
    '''my_func doc text..'''
    pass

@with_wraps
def my_func2():
    '''my_func2 doc text'''
    pass

print my_func.__doc__ #=> None
print my_func.__name__  #-> __wrapper

print my_func2.__doc__  #-> my_func2 doc text
print my_func2.__name__ #-> my_func2

'''
    사용자정의 데코레이터를 만들때 @wraps 데코레이터를 쓰는 이유는,
    사용자정의 데코레이터 내부에서 인자로 전달받은 함수는 익명함수 처럼 취급되므로 디버깅이 불가능하기 때문,,
'''






