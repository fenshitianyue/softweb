# -*- coding: utf-8 -*-

import base64
import time
import json
import os

def create_session_id():
    return base64.encodestring(str(time.time()))[::-1][3:]

def get_session_id(request):
    return request.cookies.get('session_id', None)

class Session:
    """
    使用单例模式实现，全局共用一个 session 实例对象
    类方法push和pop会触发缓存更新机制
    """
    # Session 实例对象
    __instance = None

    def __init__(self):
        # 会话映射表
        self.__session_map__ = {}
        # 会话本地存放目录
        self.__storage_path__ = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Session, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def storage(self, session_id):
        """
        将session_id对应的数据缓存到本地，文件名为session_id
        """
        session_path = os.path.join(self.__storage_path__, session_id)
        if self.__storage_path__ is not None:
            with open(session_path, 'wb') as f:
                content = json.dumps(self.__session_map__[session_id])
                # 这是一个坑：进行base64编码后再写入文件，防止一些特定的二进制字符无法正确写入
                f.write(base64.encodestring(content.encode()))

    def load_local_session(self):
        """
        从本地缓存中加载session_id对应的数据
        """
        if self.__storage_path__ is not None:
            session_path_list = os.listdir(self.__storage_path__)
            for session_id in session_path_list:
                path = os.path.join(self.__storage_path__, session_id)
                with open(path, 'rb') as f:
                    content = f.read()
                content = base64.decodestring(content)
                self.__session_map__[session_id] = json.loads(content.decode())

    def push(self, request, item, value):
        """
        更新/添加记录
        """
        session_id = get_session_id(request)

        if session_id in self.__session_map__:
            self.__session_map__[session_id][item] = value
        else:
            self.__setattr__[session_id] = {}
            self.__session_map__[session_id][item] = value
        # 每次session变动后都将变动后的session缓存在本地
        self.storage(session_id)

    def pop(self, request, item, value=True):
        """
        删除当前会话中的某个项
        """
        session_id = get_session_id(request)
        current_session = self.__session_map__.get(get_session_id(request), {})
        if item in current_session:
            del current_session[item]
            self.storage(session_id)

# 创建全局对象session
session = Session()

