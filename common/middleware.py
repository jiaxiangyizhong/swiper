from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    '''登录验证中间件'''

    white_list = ['/api/user/vcode/fetch/',
                  '/api/user/vcode/submit/',
                  '/qiniu/callback/',
                  ]

    def process_request(self, request):
        # 检查当前路径是否在白名单中
        if request.path in self.white_list:
            return

        # 获取并检查session中的uid
        uid = request.session.get('uid')
        if not uid:
            return JsonResponse({'code': 1002, 'data': '用户未登录'})
