#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:metric.py
# author: menglong.zhou@qunar.com
# 2022/5/29 12:30
from app_ticket import models as ticket_models
from django.db.models import Q
from collections import defaultdict


class Metric(object):

    def __init__(self):
        self.context = {
            'metric_context': list(),
            'message': '',
            'status': 0,
        }

    def get_top10_longtime_ticket(self):
        metric = []
        query_obj = ticket_models.Ticket.objects.filter(
            Q(active_type=3) | Q(active_type=2)).order_by('-time_consuming')
        if query_obj.count() >= 10:
            query_obj = query_obj[:10]
        for q in query_obj.all():
            if not q.time_consuming:
                continue
            metric.append({'name': str(q.id) + '-' + q.ticket_type.type_name +
                           '-' + q.ticket_title, 'value': q.time_consuming})
        self.context['metric_context'] = metric
        return self.context

    def get_most_ticket_type(self):
        metric = []
        query_obj = ticket_models.Ticket.objects.all()
        d = defaultdict(int)
        for q in query_obj:
            key = '{0}_{1}'.format(q.ticket_type.type_name, q.ticket_title)
            d[key] += 1
        number = sorted(d.items(), key=lambda x: x[1], reverse=True)
        for x in number[:10]:
            metric.append(
                {'name': x[0],
                 'value': x[1]}
            )
        self.context['metric_context'] = metric  # 取使用次数最多的top10
        return self.context
