#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:urls.py

from django.conf.urls import url
from toexcel import views

urlpatterns = [
    url(r'^dump', views.dump),   # 测试登陆用
    url(r'^toexcel', views.dump),   # 测试登陆用
]
