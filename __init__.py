# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple
from werkzeug.wrappers import Response
from wsgi_adapter import wsgi_app

class SoftWeb:
    def __init__(self):
        self.host = '192.168.204.129'
        self.port = 1024

    def dispatch_request(self, request):
        """
        路由控制
        """
        status = 200
        headers = {
            'Server': 'softweb',
        }
        # 传递符合WSGI规范的响应体给WSGI模块
        return Response('<h1>hello world</h1>', content_type='text/html', headers=headers, status=status)

    def run(self, host=None, port=None, **options):
        """
        启动入口
        """
        # 初始化
        for key, value in options.items():
            if value is not None:
                self.__setattr__(key, value)
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        # 启动web框架
        run_simple(hostname=self.host, port=self.port, application=self, **options)

    def __call__(self, env, start_response):
        """
        本框架被 WSGI 调用入口函数的方法
        """
        return wsgi_app(self, env, start_response)
