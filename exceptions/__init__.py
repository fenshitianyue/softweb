# -*- coding: utf-8 -*-

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

