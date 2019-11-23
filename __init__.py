
from werkzeug.serving import run_simple

class softweb:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 1024

    # 路由控制
    def dispatch_request(self):
        pass

    # 启动入口
    def run(self, host=None, port=None, **options):
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

    # 本框架被 WSGI 调用入口函数的方法
    def __call__(self):
        pass
