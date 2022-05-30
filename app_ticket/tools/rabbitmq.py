#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:rabbitmq.py
# author: menglong.zhou@qunar.com
# 2022/5/29 19:02


import pika
import time
from common.config import CONF
from common.log import MAIN_LOG


class RabbitmqBase(object):

    def __init__(self):
        self.conn = None
        self.chan = None

    def connect(self):
        try:
            cert = pika.PlainCredentials(
                username=CONF['username'],
                password=CONF['password']
            )
            params = pika.ConnectionParameters(
                host=CONF['host'],
                port=CONF['port'],
                virtual_host=CONF['virtual_host'],
                credentials=cert,
                heartbeat_interval=3
            )
            self.conn = pika.BlockingConnection(params)
            self.chan = self.conn.channel()
        except Exception as _ex:
            MAIN_LOG.logger.error(
                "connect to rabbitmq failed, err: %s" %
                str(_ex))

    def declare(self, exchange, queue, routing_key):
        """如果rabbitmq是HA机群的话,不建议使用代码里创建队列的方式
        所以,建议使用rabbitmq管理界面来进行创建及绑定.
        """
        try:
            self.chan.exchange_declare(exchange=exchange,
                                       type='fanout')
        except Exception as _ex:
            MAIN_LOG.logger.error("create exchange failed, err: %s" % str(_ex))

        try:
            self.chan.queue_declare(queue=queue)
        except Exception as _ex:
            MAIN_LOG.logger.error("create queue failed, err: %s" % str(_ex))

        try:
            self.chan.queue_bind(exchange=exchange,
                                 queue=queue,
                                 routing_key=routing_key)
        except Exception as _ex:
            MAIN_LOG.logger.error(
                "bind queue to exchange failed, err: %s" %
                str(_ex))

    def close(self):
        if self.chan is not None and self.chan.is_open:
            try:
                self.chan.close()
            except Exception as _ex:
                MAIN_LOG.logger.warn('chan is closing..........%s' % str(_ex))
                pass
        self.chan = None

        if self.conn is not None and self.conn.is_open:
            try:
                self.conn.close()
            except Exception as _ex:
                MAIN_LOG.logger.warn('conn is closing..........%s' % str(_ex))
                pass
        self.conn = None

    def reconnect(self):
        self.close()
        time.sleep(3)
        MAIN_LOG.logger.info(
            "process is close now Immediately to connect...............")
        self.connect()

    def retry(self, func, times):
        result = None
        need_reconn = False
        index = 0
        while index < times:
            try:
                if need_reconn:
                    self.reconnect()
                    MAIN_LOG.logger.warn(
                        "RMQ is to establish a connection...............")
                    need_reconn = False
                result = func()
            except AttributeError as _ex:
                # NOTE(other exception on reconnect)
                MAIN_LOG.logger.info("rabbitmq reconn info: %s" % str(_ex))
                need_reconn = True
                index += 1
                continue
            except Exception as _ex:
                MAIN_LOG.logger.error("rabbitmq retry error: %r" % str(_ex))
                need_reconn = True
                index += 1
                continue
            else:
                break
        return result


class RabbitmqPublisher(RabbitmqBase):

    def confirm(self):
        self.chan.confirm_delivery()

    def push(self, exchange, routing_key, body):
        def func():
            is_succeed = self.chan.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=body
            )
            if is_succeed:
                return True
            else:
                return False
        return self.retry(func, 3)


class RabbitmqConsumer(RabbitmqBase):

    def pop(self, queue_name, ack_flag=False):
        def func():
            res = self.chan.basic_get(
                queue=queue_name,
                no_ack=ack_flag
            )
            return res
        return self.retry(func, 3)

    def ack(self, method_frame):
        self.chan.basic_ack(method_frame.delivery_tag)
