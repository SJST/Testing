# -*- coding: utf-8 -*-

# @Project  : 01_Flask'
# @File     : 01_flask应用对象的初始化参数说明.py
# @Date     : 2021-02-06
# @Author   : Administrator
# @Info     :
# @Introduce:
'''
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
'''
# @Info: __name__
'''
1. __name__:
    1.1 表示当前模块的名字, 如果 当前模块为启动模块 __name__ 存在默认值 为 __main__
    1.2 如果被导入其他模块  则 __name__ 是当前文件名
'''
# @Info: app = Flask(__name__)
'''
1.app = Flask(__name__):标识启动文件
2.如果 启动文件不存在，默认当前文件为启动文件
3.维护代码需要 尽量指定 __name__
'''
# @Info: Flask 类方法初始化参数说明
'''
    1.import_name: 导入路径 （寻找静态目录和模板）
    2.static_url_path:   访问静态资源的路径  默认值 是 static 可以换掉
    3.static_folder="static", 静态文件的目录
    4.template_folder="templates", 模板文件的目录
    *  通过 2 来确认访问的是 静态页面还是渲染模板 
'''
# @Info: 设置配置参数
'''
    1.通过配置文件设置参数
    app.config.from_pyfile('config.txt)
'''