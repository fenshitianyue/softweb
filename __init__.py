# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple
from werkzeug.wrappers import Response
from wsgi_adapter import wsgi_app
import exceptions
import utility
from route import Route
import os


# 定义常见服务器异常的响应消息
ERROR_MAP = {
    401: Response('<h1>401 Unknown or unsupported method</h1>', content_type='text/html; charset=UTF-8', status=401),  # 鉴权失败
    404: Response('<h1>404 Source not found</h1>', content_type='text/html; charset=UTF-8', status=404),  # not found
    503: Response('<h1>503 Unknown function type</h1>', content_type='text/html; charset=UTF-8', status=503),  # 响应超时
}

# 定义文件类型
TYPE_MAP = {
    'css':   'text/css',
    'js':     'text/js',
    'png':   'text/png',
    'jpg':  'text/jpeg',
    'jpeg': 'text/jpeg',
}

class ExecFunc:
    def __init__(self, func, func_type, **options):
        self.func = func
        self.func_type = func_type
        self.options = options


class SoftWeb:
    def __init__(self, static_catalog='static'):
        self.host = '192.168.204.129'
        self.port = 1024
        self.url_map = {}  # 存放 url 与 endpoint 的映射
        self.static_map = {}  # 存放 url 与静态资源的映射
        self.func_map = {}  # 存放 endpoint 与处理函数的映射
        self.static_catalog = static_catalog  # 静态资源本地存放路径
        self.route = Route(self)  # 路由装饰器

    def add_url_rule(self, url, func, func_type, endpoint=None, **options):
        if endpoint is None:
            endpoint = func.__name__
        if url in self.url_map:
            raise exceptions.URLExistError
        if endpoint in self.func_map and func_type != 'static':
            raise exceptions.EndpointExistError
        # 添加 url 与节点的映射
        self.url_map[url] = endpoint
        # 添加节点与处理函数的映射
        self.func_map[endpoint] = ExecFunc(func, func_type, **options)

    def dispatch_static(self, static_path):
        """
        静态资源路由控制：找到了返回文件，否则返回404响应
        """
        if os.path.exists(static_path):
            suffix = utility.get_file_suffix(static_path)
            doc_type = TYPE_MAP.get(suffix, 'text/plain')
            with open(static_path, 'rb') as f:
                rep = f.read()
            return Response(rep, content_type=doc_type)
        else:
            return ERROR_MAP[404]

    def dispatch_request(self, request):
        """
        路由控制
        """
        # 从 URL 中提取出文件路径
        file_path = '/' + '/'.join(request.url.split('/')[3:]).split('?')[0]
        # 通过 filepath 寻找节点
        if file_path.startswith(''.join(['/', self.static_catalog, '/'])):
            # print file_path
            # print ''.join(['/', self.static_catalog, '/'])
            # print 'enter file_path.startswith'
            endpoint = 'static'
            file_path = file_path[1:]
        else:
            print 'enter else...'
            endpoint = self.url_map.get(file_path, None)

        headers = {
            'Server': 'SoftWeb 0.1'  # Server 参数表示运行的服务名
        }
        if endpoint is None:
            return ERROR_MAP[404]
        exec_function = self.func_map[endpoint]
        if exec_function.func_type == 'route':  # 路由处理
            if request.method in exec_function.options.get('methods'):
                # 判断路由的执行函数是否需要请求体进行内部处理
                argcount = exec_function.func.__code__.co_argcount  # TODO
                if argcount > 0:
                    rep = exec_function.func(request)
                else:
                    rep = exec_function.func()
            else:  # 未知请求方法
                return ERROR_MAP[401]
        elif exec_function.func_type == 'view':  # 视图处理
            rep = exec_function.func(request)
        elif exec_function.func_type == 'static':  # 静态资源处理
            return exec_function.func(file_path)
        else:  # 未知类型处理
            return ERROR_MAP[503]

        status = 200
        content_type = 'text/html'
        return Response(rep, content_type='{0}; charset=UTF-8 '.format(content_type), headers=headers, status=status)

    def bind_view(self, url, view_class, endpoint):
        self.add_url_rule(url, func=view_class.get_func(endpoint), func_type='view')

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
        self.func_map['static'] = ExecFunc(func=self.dispatch_static, func_type='static')
        # 启动web框架
        run_simple(hostname=self.host, port=self.port, application=self, **options)

    def __call__(self, env, start_response):
        """
        本框架被 WSGI 调用入口函数的方法
        """
        return wsgi_app(self, env, start_response)
