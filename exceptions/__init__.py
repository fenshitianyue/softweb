# -*- coding: utf-8 -*-

from werkzeug.wrappers import Response

CONTENT_TYPE = 'text/html; charset=UTF-8'

# 定义常见服务器异常的响应消息
ERROR_MAP = {
    2: Response('<h1>401 File not found</h1>', content_type='text/html; charset=UTF-8', status=2),
    13: Response('<h1>401 Require read permission</h1>', content_type='text/html; charset=UTF-8', status=13),
    400: Response('<h1>400 Endpoint not exists</h1>', content_type='text/html; charset=UTF-8', status=400),
    404: Response('<h1>404 Source not found</h1>', content_type='text/html; charset=UTF-8', status=404),
    405: Response('<h1>405 Unknown or unsupported method</h1>', content_type='text/html; charset=UTF-8', status=405),
    500: Response('<h1>500 Invild server error</h1>', content_type='text/html; charset=UTF-8', status=500),
    503: Response('<h1>503 Unknown function type</h1>', content_type='text/html; charset=UTF-8', status=503),
}

class SoftWebExecption(object):
    """
    框架异常基类
    """
    def __init__(self, code=500, message='Invild server error'):
        self.code = code
        self.message = message

    def __unicode__(self):
        return self.message


# class URLExistError(SoftWebExecption):
#     """访问的URL不存在"""
#     def __init__(self, message='URL exists.'):
#         super(URLExistError, self).__init__(message)


class EndpointExistError(SoftWebExecption):
    """端点错误"""
    def __init__(self, code=400, message='Endpoint not exists.'):
        super(EndpointExistError, self).__init__(code, message)


class FileNoExistsError(SoftWebExecption):
    """文件不存在"""
    def __init__(self, code=2, message='File not found'):
        super(FileNoExistsError, self).__init__(code, message)


class RequireReadPermissionError(SoftWebExecption):
    """权限不足"""
    def __init__(self, code=13, message='Require read permission'):
        super(RequireReadPermissionError, self).__init__(code, message)


class InvaildRequestMethodError(SoftWebExecption):
    """错误的请求方式"""
    def __init__(self, code=405, message='Unknow or unsupported request method'):
        super(InvaildRequestMethodError, self).__init__(code, message)


class PageNotFoundError(SoftWebExecption):
    """页面未找到"""
    def __init__(self, code=404, message='Page not found'):
        super(PageNotFoundError, self).__init__(code, message)


class UnknownError(SoftWebExecption):
    """未知错误"""
    def __init__(self, code=500, message='Invild server error'):
        super(UnknownError, self).__init__(code, message)


# def reload(code):
#     def decorator(func):
#         ERROR_MAP[code] = func
#     return decorator

def capture(func):
    def decorator(*args, **options):
        try:
            rep = func(*args, **options)
        except SoftWebExecption as e:
            if e.code in ERROR_MAP and ERROR_MAP[e.code]:
                rep = ERROR_MAP[e.code]
                status = e.code if e.code >= 100 else 500
                return rep if isinstance(rep, Response) or rep is None else Response(rep(), content_type=CONTENT_TYPE, status=status)
            else:
                raise e
        return rep
    return decorator

