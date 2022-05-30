#!/usr/bin/python env
# -*- coding: utf-8 -*-
# Created by XinYu.Wang on 2019/6/15
# file: crypto.py
from Crypto.Cipher import AES
from Crypto import Random
import binascii
import base64
from common.config import CONF
import sys

if float(sys.version[0:3]) > 3.7:
    import time
    time.clock = time.perf_counter

key = CONF['key']

def aes_convert_ecb(mode, text):
    '''
    This func only python3.x
    ECB mode for AES convert mode must set encode or decode, key is "config.KEY"
    '''
    aes_decrypter = AES.new(key)
    if mode == "encode":
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        return str(binascii.b2a_base64(aes_decrypter.encrypt(pad(text).encode('utf-8'))), encoding='utf-8')

    if mode == "decode":
        t = aes_decrypter.decrypt(base64.b64decode(text))
        return strip_none_hex(t.strip().decode())


def aes_convert_cbc(mode, text):
    '''
    This func only python3.x
    CBC mode for AES convert mode must set encode or decode, key is "config.KEY" iv is random to decode hex 32bit
    '''
    if mode == "encode":
        BS = AES.block_size
        iv = Random.new().read(BS)
        aes_decrypter = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        aa = str(binascii.b2a_base64(aes_decrypter.encrypt(pad(text).encode('utf-8'))), encoding='utf-8')
        return "%s%s" % (aa.strip("\n"), str(binascii.hexlify(iv), encoding='utf-8'))

    if mode == "decode":
        iv = text[-32:]
        iv = iv.encode(encoding='utf-8')
        text = text[0:-32]
        aes_decrypter = AES.new(key.encode('utf-8'), AES.MODE_CBC, binascii.a2b_hex(iv))
        t = aes_decrypter.decrypt(base64.b64decode(text))
        return strip_none_hex(t.strip().decode())


def strip_none_hex(text):
    '''
    strip ascii code "0-32" and "127"
    '''
    none_hex_list = ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\x09', '\x0A', '\x0B',
                     '\x0C', '\x0D', '\x0E', '\x0F', '\x0B', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x15',
                     '\x17', '\x18', '\x19', '\x1A', '\x1B', '\x1C', '\x1D', '\x1E', '\x1F', '\x20', '\x7F']
    for i in none_hex_list:
        text = text.strip(i)
    return text


def base64_convert(mode, text):
    '''
    base64 convert mode must set encode or decode
    '''
    if mode == "encode":
        return base64.b64encode(text.encode()).decode()
    if mode == "decode":
        return base64.b64decode(text).decode()