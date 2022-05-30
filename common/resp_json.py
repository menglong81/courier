#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:resp.py
# author: menglong.zhou@qunar.com
import json

class RespJson(object):

    @classmethod
    def to_json(cls, status, msg, data={}):
        return json.dumps({'status': status, 'msg': msg, 'data': data})