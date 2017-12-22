# -*-coding: utf-8-*-

import binascii
import StringIO
import base64


import crypto
import sys
sys.modules['Crypto'] = crypto
from Crypto.Cipher import AES

class PKCS7Encoder(object):

    def __init__(self, k=16):
        self.k = k

    def decode(self, text):
        nl = len(text)
        val = int(binascii.hexlify(text[-1]), 16)
        if val > self.k:
            raise ValueError('Input is not padded or padding is corrupt')

        l = nl - val
        return text[:l]

    def encode(self, text):
        l = len(text)
        output = StringIO.StringIO()
        val = self.k - (l % self.k)
        for _ in xrange(val):
            output.write('%02x' % val)
        return text + binascii.unhexlify(output.getvalue())


def decrypt(key, input):
    iv = '\x00' * 16
    aes = AES.new(key, AES.MODE_CBC, iv)
    encoder = PKCS7Encoder()

    dec_cipher = base64.b64decode(input)
    t = aes.decrypt(dec_cipher)
    unpad_text= encoder.decode(t)
    return unpad_text


def encrypt(key, raw):
    iv = '\x00' * 16
    encoder = PKCS7Encoder()
    aes = AES.new(key, AES.MODE_CBC, iv)

    pad_text = encoder.encode(raw)
    t = aes.encrypt(pad_text)
    enc_cipher = base64.b64encode(t)
    return enc_cipher