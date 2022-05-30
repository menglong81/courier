#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:req.py
# author: menglong.zhou@qunar.com
# 2022/5/27 13:25
import requests
import json

def query_tpl():
    # 查询工单模板内容
    b = {'type_name': '监控模板', 'ticket_title': '新增2'}
    url = 'http://127.0.0.1:7777/courier/ticket/query_ticket_type'
    #headers = {'content-type': 'application/json'}
    r = requests.get(url=url, data=json.dumps(b))
    print(r.json())

def query_all_g():
    url = 'http://39.107.76.152:7777/courier/ticket/query_all_group'
    r = requests.get(url)
    print(r.json())

def create_tpl():
    url = 'http://127.0.0.1:7777/courier/ticket/create_ticket_tpl'
    body = {
        'type_name': '安装模板',
        'ticket_title': '新增2',
        'handle_user': ['sre', 'op', 'net'],
        'desc': '新增location',
        'is_auto': 0,
        'helper': "请严格按照模板填写{'host': 'xxx', 'arg': 'xyz'}",
        'extra_params': json.dumps({'host': 'xxx', 'arg': 'xyz'})
    }
    headers = {'content-type': 'application/json'}
    # headers = {'content-type': 'application/x-www-form-urlencoded'}
    r = requests.post(url=url, data=json.dumps(body), headers=headers)
    print(r.json())

def create_ticket():
    url = 'http://39.107.76.152:7777/courier/ticket/add_ticket'
    detail = '''
    location ^~/static/ {	## 这里的root需要和路径结合使用，即是映射的文件位置为 /usr/alyingboy/static
    root /usr/alyingboy/; 
    index index.html
}'''
    body = {
        'ticket_type': 'NGINX模板',
        'ticket_title': 'xxxxxx',
        'create_by': '',
        'detail': detail,
        'is_auto': '0',
        'helper': "请严格按照模板填写{'host': 'xxx', 'arg': 'xyz'}",
        'extra_params': '{"host": "xxx", "arg": "xyz"}',
    }
    headers = {'content-type': 'application/json'}
    r = requests.post(url=url, data=json.dumps(body), headers=headers)
    print(r.json())


def query_select_value():
    #url = 'http://39.107.76.152:7777/courier/ticket/query_select_value'
    url = 'http://127.0.0.1:7777/courier/ticket/query_select_value'
    r = requests.get(url)
    print(r.json())



if __name__ == '__main__':
    # test()
    query_tpl()
    #query_all_g()
    #create_tpl()
    #create_ticket()
    #query_select_value()
