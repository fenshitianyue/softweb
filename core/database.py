#!/usr/bin/env python
# -*- coding: utf-8 -*-

from softweb.dbconn import BaseDB

# 数据库的相关配置暂时写在这里

DB_USER = 'root'
DB_PASSWD = ''
DB_DATABASE = 'test'

try:
    db_conn = BaseDB(DB_USER, DB_PASSWD, DB_DATABASE)
except Exception as e:
    code, __ = e.args  # 获取异常代码
    if 1049 == code:
        create_table = """
        create table user(
        id int primary key auto_increment,
        name varchar(50) unique
        ) charset=utf8
        """
        db_conn = BaseDB(DB_USER, DB_PASSWD)
        ret = db_conn.create_db(DB_DATABASE)
        if ret.is_ok:
            ret = db_conn.choose_db(DB_DATABASE)
            if ret.is_ok:
                ret = db_conn.execute(create_table)
        if not ret.is_ok:
            db_conn.drop_db(DB_DATABASE)

            print ret.error.args
            exit()
    else:
        print e
        exit()

