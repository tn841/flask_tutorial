# -*- coding:utf-8 -*-
import time


# def gen(n):
#     i=0
#     while i< n:
#         yield i
#         i += 1
#
#
# for x in gen(5):
#     print x
#
#
#
# def sleep_func(x):
#     print 'sleep..'
#     time.sleep(1)
#     return x
#
# list = [sleep_func(x) for x in range(5)]
# for i in list:
#     print i
#
#
# gen = (sleep_func(x) for x in range(5))
# for i in gen:
#     print i


def fibonacci_func(n):
    a,b = 0, 1
    i = 0
    while True:
        #time.sleep(0.2)
        if (i > n):
            return
        yield a
        a, b = b, a+b
        i += 1

fibo = fibonacci_func(5000)

for x in fibo:
    print x





