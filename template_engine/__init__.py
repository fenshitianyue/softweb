# -*- coding: utf-8 -*-

import re
import os

pattern = r'{{(.*?)}}'

def parse_args(obj):
    """
    函数作用：匹配出所有的模板标记
    """
    comp = re.compile(pattern)
    ret = comp.findall(obj)
    # 如果结果不为空，则返回结果；否则返回一个空的元组
    return ret if ret else ()


def replace_template(app, path, **options):
    """
    函数作用：读取模板文件内容，找到模板标记并进行内容替换
    """
    content = '<h1>Not found template</h1>'
    path = os.path.join(app.template_catalog, path)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            content = f.read()
            # content = f.read().decode()
        # 解析出所有的标记
        args = parse_args(content)
        # 如果置换内容不为空
        if options:
            # 遍历所有的置换标记
            for arg in args:
                # 从标记中获取键
                key = arg.strip()
                # 如果键存在于置换数据中，则进行数据替换，否则替换为空
                content = content.replace('{{%s}}' % arg, str(options.get(key, '')))
    # 返回置换后的页面内容
    return content
