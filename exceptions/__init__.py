# -*- coding: utf-8 -*-

class SoftWebExecption(object):
    """
    框架异常基类
    """
    def __init__(self, code=500, message='Error'):
        self.code = code
        self.message = message

    def __unicode__(self):
        return self.message


class URLExistError(SoftWebExecption):
    def __init__(self, message='URL exists.'):
        super(URLExistError, self).__init__(message)


class EndpointExistError(SoftWebExecption):
    def __init__(self, message='Endpoint exists.'):
        super(EndpointExistError, self).__init__(message)
