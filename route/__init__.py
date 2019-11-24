# -*- coding: utf-8 -*-

class Route:
    def __init__(self, app):
        self.app = app

    def __call__(self, url, **options):
        if 'methods' not in options:
            options['methods'] = ['GET']

        def decorator(f):
            # 调用app内部的add_url_rule添加路由规则
            self.app.add_url_rule(url, f, 'route', **options)
            return f

        return decorator

