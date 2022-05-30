#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:log.py
# author: menglong.zhou@qunar.com

from common import config
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys


class LogBase(object):
    def __init__(self, log_name, mode, level, rotating=True, when='MIDNIGHT'):
        self.log_path = config.CONF['log_path']

        if os.path.exists(self.log_path) is False:
            os.mkdir(self.log_path)

        self.log_level = level
        self.logger = logging.getLogger(log_name)

        if self.log_level == 'DEBUG':
            formatter = logging.Formatter('%(asctime)s %(module)s %(funcName)s %(levelname)-8s: %(message)s')
        else:
            formatter = logging.Formatter('%(asctime)s %(module)s %(levelname)-8s: %(message)s')

        if rotating is True:    # 日志轮转默认按天
            self.file_handler = TimedRotatingFileHandler(os.path.join(self.log_path, log_name), when)
        else:   # 不轮转
            self.file_handler = logging.FileHandler(os.path.join(self.log_path, log_name))

        self.file_handler.setFormatter(formatter)
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.formatter = formatter
        self.logger.setLevel(getattr(logging, self.log_level))
        if mode == 'file':
            self._register_file()
        elif mode == 'console':
            self._register_console()
        elif mode == 'all':
            self._register_console()
            self._register_file()
        print('register {log_name}'.format(log_name=log_name))

    def _register_file(self):
        self.logger.addHandler(self.file_handler)

    def _register_console(self):
        self.logger.addHandler(self.console_handler)


MAIN_LOG = LogBase('%s.log' % (config.CONF['site_name']), 'all', config.CONF['log_level'])