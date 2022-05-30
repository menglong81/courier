#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:ticket.py
# author: menglong.zhou@qunar.com
# 2022/5/27 11:55
import json
from django.shortcuts import render
from app_ticket.lib.ticket import Ticket
from django.shortcuts import HttpResponse
from common.resp_json import RespJson


def create_ticket_type(request):
    body = request.body or {}
    data = json.loads(body)
    resp = Ticket().create_ticket_type(**data)
    return HttpResponse(RespJson.to_json('ok', 'ok', data=resp))


def add_ticket(request):
    body = request.body or {}
    data = json.loads(body)
    resp = Ticket().create_ticket(**data)
    return HttpResponse(RespJson.to_json('ok', 'ok', data=resp))


def query_ticket_type(request):
    type_name = request.GET.get('type_name')
    ticket_title = request.GET.get('ticket_title')
    data = {'type_name': type_name, 'ticket_title': ticket_title}
    resp = Ticket().query_ticket_type(**data)
    return HttpResponse(RespJson.to_json('ok', 'ok', data=resp))


def query_select_value(request):
    resp = Ticket().query_select_value()
    return HttpResponse(RespJson.to_json('ok', 'ok', data=resp))


def add_tpl(request):
    return render(request, 'ticket/createtask.html')


def submit_ticket(request):
    user = {'user': request.user.username}
    return render(request, 'ticket/add_ticket.html', user)


def summary(request):
    return render(request, 'metrics/echarts.html')
