#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:groups.py
# author: menglong.zhou@qunar.com
# 2022/5/27 13:43
from django.contrib.auth.models import Group


class GroupManger(object):
    def __init__(self):
        self.context = {
            'groups': list(),
            'status': 0
        }

    def query_all_group(self, *args, **kwargs):
        for g in Group.objects.all():
            self.context['groups'].append(g.name)
        return self.context
