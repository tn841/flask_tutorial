#-*- coding:utf-8 -*-

def func1(*args):
    for arg in args:
        print arg


func1(1,2,3,4,5)


def func2(**kwargs):
    for key, val in kwargs:
        print key,
        print val

func2(k1='val1', k2='val2', k3='val3')


def func3(*args, **kwargs):
    print args,
    print kwargs


func3(1,3,key1='val1', key4='val4')

def func4(a,b,c):
    print a,b,c

p = ['a','b','c']
func4(*p)

p2={'a':'1', 'b':2, 'c':3}
func4(**p2)