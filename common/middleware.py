#!/usr/bin/python env
# -*- coding: utf-8 -*-
# Created by XinYu.Wang on 2019/6/15
# file: middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from common import crypto
from common.config import CONF
from common.log import MAIN_LOG
from common.crypto import aes_convert_cbc as aes_convert

import json
import time
import re

APP_NAME = CONF['site_name']
class CookieAuth(MiddlewareMixin):
    if CONF.get('admin_mode') is True:
        check_flag = 'off'
    else:
        check_flag = 'on'      # 设置一个开关，方便调试, OFF|和ON 只是不验证cookie，其他功能依旧可以使用

    white_list = [
        '/%s/ticket/' % APP_NAME,
        '/%s/usercenter/login.html' % APP_NAME,
        '/%s/usercenter/logout.html' % APP_NAME,
        '/%s/usercenter/wechat_callback.html' % APP_NAME,
        '/%s/usercenter/wechat_create_menu.html' % APP_NAME,
        '/%s/usercenter/notrss.html' % APP_NAME,
        '/media/%s/' % APP_NAME,
        '/%s/tools/' % APP_NAME,
        '/%s/toexcel/' % APP_NAME,
        '/static/',
    ]

    def process_request(self, request):

        if 'login' in request.__dict__['path'] or 'logout' in request.__dict__['path']:
            return None

        if '/%s/admin' % APP_NAME in request.__dict__['path']:
            return None

        for w in CookieAuth.white_list:
            if w in request.__dict__['path']:
                return None

        if request.__dict__['path'] in CookieAuth.white_list:
            return CookieAuth._auth_cookie(request)

        return CookieAuth._auth_cookie(request)

    def process_response(self, request, response):
        if 'logout.html' in request.__dict__['path']:
            return CookieAuth._logout(request, response)

        if request.__dict__.get("set_cookie") is True:
            cookie_val = [int(time.time()), request.__dict__.get("set_cookie_user"), int(time.time())]
            data = crypto.base64_convert("encode", aes_convert("encode", json.dumps(cookie_val)))
            response.set_signed_cookie('s', data, path='/')
            return response

        return CookieAuth._update_cookie(request, response)


    @classmethod
    def _auth_cookie(cls, request):
        if cls.check_flag.lower() == 'off':
            return None

        last_url = request.get_full_path()

        if 'micromessenger' in request.META.get('HTTP_USER_AGENT', '').lower():
            redict_url = redirect('/%s/usercenter/login.html?last_url=%s' % (APP_NAME, last_url))
        else:
            redict_url = redirect('/%s/usercenter/dev_login.html?last_url=%s' % (APP_NAME, last_url))

        if request.__dict__["META"]["PATH_INFO"].split("/")[1] == "api":
            api_flag = True
        else:
            api_flag = False
        try:
            data_cookie = request.COOKIES.get('s', None)
            if data_cookie is None: return redict_url
            data_cookie = json.loads(aes_convert("decode", crypto.base64_convert("decode", data_cookie.split(":")[0])))
        except Exception as e:
            print(e)
            return redict_url

        if data_cookie[0] == "error":
            return redict_url

        if CONF.get('min_action_time') == -1:
            pass
        elif (int(time.time()) - int(data_cookie[2])) > CONF.get('min_action_time'):
            if api_flag: return HttpResponse(json.dumps(["Error", "登录已过期，请重新登录！"]))
            return redict_url

        funvar = {"user_name": data_cookie[1], "login_time": data_cookie[0],
                  "cookies": request.COOKIES.get('s'), "user_table_id": -1, "last_action": data_cookie[2]}

        request.__dict__["website_cookie"] = funvar
        return None

    @classmethod
    def _update_cookie(cls, request, respone):
        '''
        更新cookie，并且刷新用户最后的活动时间
        '''
        if cls.check_flag.lower() == 'off':
            return respone

        funcvar = request.__dict__.get("website_cookie")
        if funcvar is None:
            return respone
        cookie_val = [funcvar["login_time"], funcvar["user_name"], int(time.time())]
        data = crypto.base64_convert("encode", aes_convert("encode", json.dumps(cookie_val)))
        respone.set_signed_cookie('s', data, path='/')
        return respone

    @classmethod
    def _logout(cls, request, respone):
        '''
        把cookie设置成3个error，退出登陆
        '''
        cookie_val = ["error", "error", "error", ]
        data = crypto.base64_convert("encode", aes_convert("encode", json.dumps(cookie_val)))
        obj = redirect('/%s/usercenter/login.html' % APP_NAME)
        # respone.set_signed_cookie('s', data, path='/')
        obj.set_signed_cookie('s', data, path='/')
        return obj