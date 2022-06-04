#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:ticket.py
# author: menglong.zhou@qunar.com
# 2022/5/27 11:57
import json
from django.contrib.auth.models import Group
from app_ticket import models as ticket_models
from app_ticket.tools.rabbitmq import RabbitmqPublisher
from common.config import CONF


class Ticket(object):

    def __init__(self):
        self.context = {
            'ticket_type_context': list(),
            'message': '',
            'status': 0,
            'query_result': dict()
        }

    def show_ticket_type(self, *args, **kwargs):
        ticket_type_obj = ticket_models.TicketType.objects.all()
        for ticket in ticket_type_obj:
            _tmp = {
                'type_name': ticket.type_name,
                'ticket_title': ticket.ticket_title,
                'desc': ticket.desc,
                'is_auto': ticket.is_auto,
                'helper': ticket.helper,
                'extra_params': ticket.extra_params,
                'handle_user': ticket.handle_user,
            }
            self.context['ticket_type_context'].append(_tmp)
        return self.context

    def query_ticket_type(self, *args, **kwargs):
        type_name = kwargs.get('type_name') or '标准模板'
        ticket_title = kwargs.get('ticket_title')
        ticket_type_obj = ticket_models.TicketType.objects.get(
            type_name=type_name, ticket_title=ticket_title)
        g = Group.objects.all()

        handle_group = []
        for _g in ticket_type_obj.handle_user.filter(id__in=g):
            handle_group.append(_g.name)

        _tmp = {
            'type_name': ticket_type_obj.type_name,
            'ticket_title': ticket_type_obj.ticket_title,
            'desc': ticket_type_obj.desc,
            'is_auto': ticket_type_obj.is_auto,
            'helper': ticket_type_obj.helper,
            'extra_params': ticket_type_obj.extra_params,
            'handle_user': handle_group,
        }
        self.context['ticket_type_context'].append(_tmp)
        return self.context

    def query_select_value(self):
        tpl = ticket_models.TicketType.objects.all()
        ret = {}
        for p in tpl:
            if p.type_name not in ret:
                ret[p.type_name] = []
            ret[p.type_name].append(p.ticket_title)
        self.context['query_result'] = ret
        return self.context

    def create_ticket_type(self, *args, **kwargs):
        ticket_type_obj = ticket_models.TicketType.objects.filter(
            type_name=kwargs.get('type_name'), ticket_title=kwargs.get('ticket_title'))
        if ticket_type_obj:
            self.context['status'] = 1
            self.context['message'] = '已存在相同模板'
            return self.context
        _tmp = {
            'type_name': kwargs.get('type_name'),
            'ticket_title': kwargs.get('ticket_title'),
            'desc': kwargs.get('desc'),
            'is_auto': kwargs.get('is_auto') or 1,
            'helper': kwargs.get('helper'),
            'extra_params': kwargs.get('extra_params'),
        }
        ticket_type_obj.create(**_tmp)
        handle_user = kwargs.get('handle_user')
        for user in handle_user:
            for g in Group.objects.filter(name=user).all():
                for i in ticket_type_obj.all():
                    i.handle_user.add(g)
        return self.context

    def create_ticket(self, *args, **kwargs):
        ticket_type = kwargs.get('ticket_type')
        tid = ticket_models.TicketType.objects.get(type_name=ticket_type)
        _tmp = {
            'ticket_type': tid,
            'ticket_title': kwargs.get('ticket_title'),
            'create_by': kwargs.get('create_by'),
            'detail': kwargs.get('detail'),
            'is_auto': kwargs.get('is_auto'),
            'extra_params': kwargs.get('extra_params'),
        }
        ticket_models.Ticket.objects.create(**_tmp)

        # TODO 增加rmq通知
        # if kwargs.get('is_auto') == 0 and CONF['rmq_enable']:
        #     publisher = RabbitmqPublisher()
        #     publisher.connect()
        #     publisher.confirm()
        #     body = json.dumps(_tmp)
        #
        #     publisher.push(CONF['exchange'], CONF['routing_key'], body)
        #     publisher.close()

        return self.context
