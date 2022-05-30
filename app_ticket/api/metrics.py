#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:metrics.py
# author: menglong.zhou@qunar.com
# 2022/5/29 12:43

from app_ticket.lib.metric import Metric
from django.shortcuts import HttpResponse
from common.resp_json import RespJson


def get_top10_longtime_ticket(request):
    resp = Metric().get_top10_longtime_ticket()
    response = HttpResponse(RespJson.to_json('ok', 'ok', data=resp))
    response['Access-Control-Allow-Origin'] = '*'
    return response


def get_most_ticket_type(request):
    resp = Metric().get_most_ticket_type()
    response = HttpResponse(RespJson.to_json('ok', 'ok', data=resp))
    response['Access-Control-Allow-Origin'] = '*'
    return response
