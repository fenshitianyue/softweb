# -*- coding: utf-8 -*-

import pymysql


class DBResult:
    """
    数据库返回的结果对象，类似django的queryset
    """
    exists = False    # 执行成功与否
    result = None     # 查询结果集：[{...} ...]
    error = None      # 异常信息
    rows = None       # 影响行数

    def index_of(self, index):
        if self.exists and isinstance(index, int) and index < self.rows and index >= -self.rows:
            return self.result[index]

    def get_first(self):
        return self.index_of(0)

    def get_last(self):
        return self.index_of(-1)

    @staticmethod
    def handler(func):
        """ 异常捕获装饰器 """
        def decorator(*args, **options):
            ret = DBResult()
            try:
                ret.rows, ret.result = func(*args, **options)
                ret.exists = True
            except Exception as e:
                ret.error = e
            return ret
        return decorator


class BaseDB:

    def __init__(self, user, passwd, database='', host='127.0.0.1',
                 port=3306, charset='utf8', cursor_class=pymysql.cursors.DictCursor):
        """参数说明：
        @host: 默认为 127.0.0.1
        @port: 默认为 3306
        @charset: 默认为 utf8
        """
        self.user = user
        self.passwd = passwd
        self.database = database
        self.host = host
        self.port = port
        self.charset = charset
        self.cursor_class = cursor_class
        self.conn = self.connect()

    def connect(self):
        return pymysql.connect(host=self.host, user=self.user, port=self.port,
                               passwd=self.passwd, db=self.database,
                               charset=self.charset, cursorclass=self.cursor_class)

    def close(self):
        self.conn.close()

    def execute(self, sql, params=None):
        pass

    def create_db(self, db_name, db_charset='utf8'):
        pass

    def choose_db(self, db_name):
        pass

    def insert(self, sql, params=None):
        pass

    def drop_db(self, db_name):
        pass

