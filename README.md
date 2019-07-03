# flask-pluginkit-footprint
足迹生成插件

### 功能

输入去过的地方可导出HTML文档，也可以按照用户名保存生成专属页面，使用短网址`用户名.love`访问主页

### 安装

`pip install git+https://github.com/flask-pluginkit/flask-pluginkit-footprint@master`

### 配置

**配置读取的是项目根目录下config.py模块中`PLUGINS`配置段(dict)，以下是key：**

1. 可选参数`PLUGINKIT_FOOTPRINT_KEY`，这是百度地图开放平台js端ak！

    > 插件首先使用current_app.config['PLUGINKIT_FOOTPRINT_KEY']尝试读取此配置；未发现时从项目config模块读取PLUGINS['PLUGINKIT_FOOTPRINT_KEY']，否则使用默认值。

2. 可选参数`PLUGINKIT_FOOTPRINT_REDIS_URL`，这是redis连接信息，DSN-Style

3. 可选参数`PLUGINKIT_FOOTPRINT_REDIS_CONNECTION`，同上，redis连接类的实例

    > 上面两个参数以使用redis存储用户生成专属页的页面代码，首选url、次选connection，这两个参数如果有任何一个有效，就会使用redis，否则使用Local本地存储。

### 使用

此插件依赖[Flask-PluginKit](https://github.com/staugur/flask-pluginkit "Flask-PluginKit")，使用时请在初始化PluginManager时传入plugin_packages参数(类型list)，加上"flask_pluginkit_footprint"！

插件包含一个蓝图，路由前缀是`/footprint`；包含两个tep导航，不过是针对性的，如果需要访问插件首页，可以使用`url_for('footprint.index')`

参考文档：[Flask-PluginKit third-party-plugin](https://flask-pluginkit.readthedocs.io/zh_CN/latest/#third-party-plugin "third-party-plugin")

### 感谢

此插件是基于[shengxinjing/footprint](https://github.com/shengxinjing/footprint)的js版二次开发，感谢原作者！
