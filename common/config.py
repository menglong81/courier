#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file:config.py
# author: menglong.zhou@qunar.com

import yaml
import sys
import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config(dict):
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = dict.__new__(cls)
            return cls._instance
        return cls._instance

    def __init__(self):
        super(Config, self).__init__()
        if not hasattr(self, 'lock'):
            self.lock = True
            self.range = dict()
            self._default()
            self._load_conf_file()
            self._check_config()

    def _win32_conf(self):
        self.__setitem__('log_path', "D:\\logs\\courier")

    def _default(self):
        self.__setitem__('log_level', 'DEBUG', ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
        self.__setitem__('log_path', '/home/q/logs/courier')
        if sys.platform == "win32":
            self._win32_conf()

    def _load_conf_file(self):
        self.conf_path = [os.path.join(BASE_DIR, "conf", "main.conf"), ]

        for p in self.conf_path:
            if os.path.isfile(p):
                self.update(yaml.load(open(p, "r")))
                break
        else:
            logging.error("Don't find config file")
            exit(1)

        if sys.platform == "win32":
            self._win32_conf()

    def _check_config(self):
        for k in self:
            if self.range.get(k, None) is not None:
                if self[k] not in self.range[k]:
                    raise ValueError('Config "{k}: {v}" invalid, reference "{r}"'.format(k=k, v=self[k], r='|'.join(self.range[k])))

    def __setitem__(self, key, value, value_range=None):
        if value_range is not None:
            self.range[key] = value_range
        super(Config, self).__setitem__(key, value)


CONF = Config()