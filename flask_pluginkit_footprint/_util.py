# -*- coding: utf-8 -*-
"""
    Flask-PluginKit-Footprint._util
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    工具

    :copyright: (c) 2019 by staugur.
    :license: BSD, see LICENSE for more details.
"""

from flask_pluginkit import LocalStorage, RedisStorage


class Storage():

    def __init__(self, redis_url=None, redis_connection=None):
        if redis_url or redis_connection:
            self._storage = RedisStorage(redis_url, redis_connection)
        else:
            self._storage = LocalStorage()

    def gen_key(self, unique_name):
        if unique_name:
            return "flask_pluginkit_footprint:%s" % unique_name

    def make_love(self, unique_name, html):
        """存储一个专属页面"""
        key = self.gen_key(unique_name)
        if key and html:
            return self._storage.set(key, html)
        raise ValueError

    def has_love(self, unique_name):
        key = self.gen_key(unique_name)
        if key:
            data = self._storage.list or {}
            if key in data.keys():
                return True
        return False

    def find_love(self, unique_name):
        """查询专属页"""
        key = self.gen_key(unique_name)
        if key:
            html = self._storage.get(key)
            if not html:
                raise ValueError
            else:
                return html
        raise ValueError
