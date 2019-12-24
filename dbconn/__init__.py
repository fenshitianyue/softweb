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

    @DBResult.handler
    def execute(self, sql, params=None):
        with self.conn as cursor:
            rows = cursor.execute(sql, params) if params and isinstance(params, dict) else cursor.execute(sql)
            result = cursor.fetchall()
            return rows, result

    def create_db(self, db_name, db_charset='utf8'):
        sql = 'create database {} default character set {}'.format(db_name, db_charset)
        return self.execute(sql)

    @DBResult.handler
    def choose_db(self, db_name):
        self.conn.select_db(db_name)
        # 这里因为执行结果并没有影响数据，所以返回两个空值
        return None, None

    def insert(self, sql, params=None):
        ret = self.execute(sql, params)
        ret.result = self.conn.insert_id()
        return ret

    def drop_db(self, db_name):
        sql = 'drop database {}'.format(db_name)
        return self.execute(sql)

