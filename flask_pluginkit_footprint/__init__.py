# -*- coding: utf-8 -*-
"""
    Flask-PluginKit-Footprint
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    足迹生成

    :copyright: (c) 2019 by staugur.
    :license: BSD, see LICENSE for more details.
"""

#: Importing these two modules is the first and must be done.
#: 首先导入这两个必须模块
from __future__ import absolute_import
#: Import the other modules here, and if it's your own module, use the relative Import. eg: from .lib import Lib
#: 在这里导入其他模块, 如果有自定义包, 使用相对导入, 如: from .lib import Lib
import os, hashlib
from flask import Blueprint, render_template, render_template_string, request, jsonify, current_app, url_for, abort
from ._util import Storage
try:
    from config import PLUGINS
except ImportError:
    PLUGINS = {}

#: Your plug-in name must be consistent with the plug-in directory name.
#: 你的插件名称，不严格要求和插件目录名称保持一致.
__plugin_name__ = "flask-pluginkit-footprint"
#: Plugin describes information. What does it do?
#: 插件描述信息,什么用处.
__description__ = "足迹生成器"
#: Plugin Author
#: 插件作者
__author__      = "Mr.tao <staugur@saintic.com>"
#: Plugin Version
#: 插件版本
__version__     = "0.1.0"
#: Plugin Url
#: 插件主页
__url__         = "https://github.com/flask-pluginkit/flask-pluginkit-footprint"
#: Plugin License
#: 插件许可证
__license__     = "BSD 3"
#: 插件状态, enabled、disabled
__state__       = "enabled"

pb = Blueprint("footprint", "footprint")
md5 = lambda pwd:hashlib.md5(pwd).hexdigest()
storage = Storage(PLUGINS.get("PLUGINKIT_FOOTPRINT_REDIS_URL"), PLUGINS.get("PLUGINKIT_FOOTPRINT_REDIS_CONNECTION"))

@pb.route("/")
def index():
    FOOTPRINT_KEY = PLUGINS.get("PLUGINKIT_FOOTPRINT_KEY")
    if "PLUGINKIT_FOOTPRINT_KEY" in current_app.config:
        FOOTPRINT_KEY = current_app.config["PLUGINKIT_FOOTPRINT_KEY"]
    if not FOOTPRINT_KEY:
        FOOTPRINT_KEY = "fHrNQj6DHTjZtfTvfqbsuvTzKc5V9SBl"
    return render_template("footprint/footprint.html", FOOTPRINT_KEY=FOOTPRINT_KEY)

@pb.route("/<name>.love")
def love(name):
    if name:
        unique_name = md5(name)
        if storage.has_love(unique_name):
            try:
                html = storage.find_love(unique_name)
            except Exception as e:
                current_app.logger.debug(e, exc_info=True)
                return render_template_string("程序异常，请稍后重试！")
            else:
                return render_template_string(html)
    return abort(404)

@pb.route("/make_love", methods=["POST"])
def make_love():
    if request.method == "POST":
        res = dict(code=1, msg=None)
        data = request.json
        if data and isinstance(data, dict) and data.get("name") and data.get("html"):
            # 接收参数
            name = data["name"]
            html = data["html"]
            unique_name = md5(name)
            if storage.has_love(unique_name):
                res.update(msg="专属名称已存在", text="The exclusive name already exists")
            else:
                try:
                    storage.make_love(unique_name, html)
                except:
                    res.update(msg="无法保存专属页", text="Unable to save exclusive pages")
                else:
                    res.update(code=0, long_url=url_for("footprint.love", name=name, _external=True), name=name, unique_name=unique_name)
        else:
            res.update(msg="请求参数不合法", text="Invalid request parameters")
        return jsonify(res)

#: 返回插件主类
def getPluginClass():
    return PluginFootprintMain

#: 插件主类, 请保证getPluginClass准确返回此类
class PluginFootprintMain(object):

    def register_bep(self):
        """注册蓝图入口, 返回蓝图路由前缀及蓝图名称"""
        bep = {"prefix": "/footprint", "blueprint": pb}
        return bep

    def register_tep(self):
        return dict(openservice_navigation='footprint/nav.html', index_openservice_navigation='footprint/nav_index.html')
