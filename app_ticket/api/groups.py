#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:groups.py
# author: menglong.zhou@qunar.com
# 2022/5/27 16:45

from app_ticket.lib.groups import GroupManger
from django.shortcuts import HttpResponse
from common.resp_json import RespJson


def query_all_group(request):
    resp = GroupManger().query_all_group()
    return HttpResponse(RespJson.to_json('ok', 'ok', data=resp))
