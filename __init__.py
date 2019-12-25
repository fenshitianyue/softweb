# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple
from werkzeug.wrappers import Response
from wsgi_adapter import wsgi_app
import exceptions
import utility
from route import Route
from template_engine import replace_template
from session import create_session_id, session
# import view
import json
import os

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
    template_catalog = None  # 类属性，模板文件本地存放目录

    def __init__(self, static_catalog='static', template_catalog='template', session_path='.session'):
        self.host = '192.168.204.129'
        self.port = 1024
        self.url_map = {}                                       # 存放 url 与 endpoint 的映射
        self.static_map = {}                                    # 存放 url 与静态资源的映射
        self.func_map = {}                                      # 存放 endpoint 与处理函数的映射
        self.static_catalog = static_catalog                    # 静态资源本地存放路径
        self.template_catalog = template_catalog                # 模板文件本地存放路径
        SoftWeb.template_catalog = self.template_catalog        # 初始化类的属性，供置换模板引擎调用
        self.route = Route(self)                                # 路由装饰器
        self.session_path = session_path                        # 会话的session缓存路径

    def add_url_rule(self, url, func, func_type, endpoint=None, **options):
        if endpoint is None:
            endpoint = func.__name__
        if url in self.url_map:
            # raise exceptions.URLExistError
            raise exceptions.PageNotFoundError
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
            raise exceptions.FileNoExistsError

    def dispatch_request(self, request):
        """
        路由控制
        """
        # 从 URL 中提取出文件路径
        file_path = '/' + '/'.join(request.url.split('/')[3:]).split('?')[0]
        # 通过 filepath 寻找节点
        # if file_path.find(self.static_catalog) == 1 and file_path.index(self.static_catalog) == 1:
        if file_path.startswith(''.join(['/', self.static_catalog, '/'])):
            # print file_path
            # print ''.join(['/', self.static_catalog, '/'])
            # print 'enter file_path.startswith'
            endpoint = 'static'
            file_path = file_path[1:]
        else:
            # print 'enter else...'
            endpoint = self.url_map.get(file_path, None)

        cookies = request.cookies
        # 如果此次请求中没有session_id，则在HTTP报文响应头中添加此次生成的唯一性session_id
        if 'session_id' not in cookies:
            headers = {
                'Server': 'SoftWeb 0.1',  # Server 参数表示运行的服务名
                'Set-Cookie': 'session_id=%s' % create_session_id(),
            }
        else:
            headers = {
                'Server': 'SoftWeb 0.1',
            }
        if endpoint is None:
            raise exceptions.EndpointExistError
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
                raise exceptions.InvaildRequestMethodError
        elif exec_function.func_type == 'view':  # 视图处理
            rep = exec_function.func(request)
        elif exec_function.func_type == 'static':  # 静态资源处理
            return exec_function.func(file_path)
        else:  # 未知类型处理
            raise exceptions.UnknownError

        # 如果rep是Response类型，说明是重定向结果，直接返回
        if isinstance(rep, Response):
            return rep

        status = 200
        content_type = 'text/html'
        return Response(rep, content_type='{0}; charset=UTF-8 '.format(content_type), headers=headers, status=status)

    def bind_view(self, url, view_class, endpoint):
        self.add_url_rule(url, func=view_class.get_func(endpoint), func_type='view')

    def load_controller(self, controller):
        name = controller.__name__()  # TODO:这里回头把controller中获取名字的方法改一下，容易误导__name__是一个属性
        # 遍历映射关系，将映射关系添加到类的 url_map 方法中
        for rule in controller.url_map:
            # 绑定 URL 与 视图函数，节点的命名格式：控制器名 + . + 节点名
            self.bind_view(rule['url'], rule['view'], ''.join([name, '.', rule['endpoint']]))

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
        # 映射静态资源处理函数（所有静态资源处理函数都是静态资源路由）
        self.func_map['static'] = ExecFunc(func=self.dispatch_static, func_type='static')

        # 如果会话session目录不存在，则创建
        if not os.path.exists(self.session_path):
            os.mkdir(self.session_path)

        # 设置会话session存放目录
        session.set_storage_path(self.session_path)
        session.load_local_session()

        # 启动web框架
        run_simple(hostname=self.host, port=self.port, application=self, **options)

    def __call__(self, env, start_response):
        """
        本框架被 WSGI 调用入口函数的方法
        """
        return wsgi_app(self, env, start_response)


def simple_template(path, **options):
    """
    模板渲染的接口
    """
    return replace_template(SoftWeb, path, **options)


def redirect(url, status_code=302):
    """
    url重定向接口，默认为临时重定向
    """
    response = Response('', status=status_code)
    response.headers['Location'] = url

    return response


def render_json(data):
    """
    以json格式返回数据接口
    """
    content_type = 'text/plain'
    if isinstance(data, dict) or isinstance(data, list):
        data = json.dumps(data)
        content_type = 'application/json'
    return Response(data, content_type='{0}; charset=UTF-8'.format(content_type), status=200)

def render_file(file_path, file_name=None):
    """
    文件下载接口
    """
    if os.path.exists(file_path):
        if not os.access(file_path, os.R_OK):
            raise exceptions.RequireReadPermissionError
        with open(file_path, 'rb') as f:
            content = f.read()

        if file_name is None:
            file_name = file_path.split('/')[-1]

        headers = {
            'Content-Disposition': 'attachment; filename={0}'.format(file_name)
        }
        return Response(content, headers=headers, status=200)
    raise exceptions.FileNoExistsError

