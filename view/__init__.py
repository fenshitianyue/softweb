# -*- coding: utf-8 -*-

class View(object):
    methods = None
    methods_meta = None

    def dispath_request(self, request, *args, **kwargs):
        """
        视图处理函数调度入口
        """
        raise NotImplementedError

    @classmethod
    def get_func(cls, name):
        """
        生成视图处理函数
        """
        def func(*args, **kwargs):
            obj = func.view_class()
            return obj.dispath_request(*args, **kwargs)

        func.view_class = cls
        func.__name__ = name
        func.__doc__ = cls.__doc__
        func.__module__ = cls.__module__
        func.methods = cls.methods
        return func

class Controller:
    def __init__(self, name, url_map):
        self.url_map = url_map  # 存放映射关系的结构 -> [{...},{...},...]
        self.name = name  # 控制器的名字，在生成 endpoint 时区分不同控制器下同名的视图对象

    def __name__(self):
        return self.name
