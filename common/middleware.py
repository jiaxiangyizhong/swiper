import logging

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from User.models import User
from common import errors
from libs.http import render_json

err_log = logging.getLogger('err')


class AuthMiddleware(MiddlewareMixin):
    '''登录验证中间件'''

    white_list = ['/api/user/vcode/fetch/',
                  '/api/user/vcode/submit/',
                  '/qiniu/callback/',
                  '/',
                  ]

    def process_request(self, request):
        # 检查当前路径是否在白名单中
        if request.path in self.white_list:
            return

        # 获取并检查session中的uid
        uid = request.session.get('uid')
        if not uid:
            return JsonResponse({'code': errors.LoginRequired, 'data': '用户未登录'})
        else:
            request.uid = uid


class LogicErrMiddleware(MiddlewareMixin):
    '''逻辑异常处理中间件'''

    def process_exception(self, request, exception):
        if isinstance(exception, errors.LogicErr):
            err_log.error(f'逻辑异常:{exception.code}:{exception.data}')
            return render_json(exception.data, exception.code)
