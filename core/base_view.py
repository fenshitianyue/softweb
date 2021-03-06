# -*- coding: utf-8 -*-

from softweb.view import View
from softweb.session import AuthSession, session
from softweb import redirect

class BaseView(View):
    """
    不需要鉴权的视图继承此类
    """
    methods = ['GET', 'POST']

    def get(self, request, *args, **options):
        pass

    def post(self, request, *args, **options):
        pass

    # 视图处理函数调度入口
    def dispatch_request(self, request, *args, **options):
        methods_meta = {
            'GET': self.get,
            'POST': self.post,
        }
        if request.method in methods_meta:
            return methods_meta[request.method](request, *args, **options)
        else:
            return '<h1>Unknown or unsupported require method.</h1>'


class AuthLogin(AuthSession):

    @staticmethod
    def auth_logic(request, *args, **options):
        if 'user' in session.map(request):
            return True
        return False

    @staticmethod
    def auth_fail_callback(request, *args, **options):
        return redirect('/login')


class SessionView(BaseView):
    """
    需要鉴权的视图继承此类
    """
    @AuthLogin.auth_session
    def dispatch_request(self, request, *args, **options):
        return super(SessionView, self).dispatch_request(request, *args, **options)
