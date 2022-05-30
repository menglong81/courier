#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:urls.py
from django.conf.urls import url
from app_ticket.api import ticket, groups, metrics
urlpatterns = [

    # Ticket
    url(r'create_ticket_tpl', ticket.create_ticket_type),
    url(r'add_ticket', ticket.add_ticket),
    url(r'query_ticket_type', ticket.query_ticket_type),
    url(r'query_select_value', ticket.query_select_value),
    # HTML
    url(r'add_tpl.html', ticket.add_tpl),
    url(r'submit_ticket.html', ticket.submit_ticket),
    url(r'summary.html', ticket.summary),

    # Metrics
    url(r'get_top10_longtime_ticket', metrics.get_top10_longtime_ticket),
    url(r'get_most_ticket_type', metrics.get_most_ticket_type),


    # Group
    url(r'query_all_group', groups.query_all_group),


]
