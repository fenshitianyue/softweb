# -*- coding: utf-8 -*-

from werkzeug.wrappers import Request

def wsgi_app(app, env, start_response):
    """
    功能描述：WSGI 调度框架入口
    :param1 应用
    :param2 服务器传过来的请求
    :param3 响应载体，这个参数不会用到，只是框架需求
    """
    # 解析请求头
    request = Request(env)
    # 把请求传递给框架的路由控制进行处理，并获取处理结果
    response = app.dispatch_request(request)
    # 返回给服务器
    return response(env, start_response)
