#!/usr/bin/env python
# -*- coding: utf-8 -*-

from softweb import SoftWeb

app = SoftWeb()

@app.route('/index', methods=['GET'])
def index():
    return 'This is a test route page.'

@app.route('/test/js')
def test_static_js():
    return '<script src="/static/test.js"></script>'

@app.route('/js')
def test_js():
    return 'test /js'


if __name__ == '__main__':
    app.run()
