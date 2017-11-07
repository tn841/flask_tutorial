#-*- coding:utf-8 -*-

from passlib.hash import sha256_crypt

password = sha256_crypt.encrypt("password")
password2 = sha256_crypt.encrypt("password")
password3 = sha256_crypt.encrypt("danal")
password4 = sha256_crypt.encrypt("danal")
password5 = sha256_crypt.encrypt("danal")

print(password)
print(password2)
print(password3)
print(password4)
print(password5)

print(sha256_crypt.verify("password", password))
print(sha256_crypt.verify("password", password2))
print(sha256_crypt.verify("danal", password3))
print(sha256_crypt.verify("danal", password4))
print(sha256_crypt.verify("danal", password5))