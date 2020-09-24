from django.core.cache import cache
from django.http import JsonResponse
from User.logic import send_vcode
from User.models import User, Profile


def fetch_vcode(request):
    '''给用户发送验证码'''
    phonenum = request.GET.get('phonenum')
    if send_vcode(phonenum):
        return JsonResponse({'code': 0, 'data': None})
    return JsonResponse({'code': 1000, 'data': '验证码发送失败'})


def submit_vcode(request):
    '''提交验证码，执行登录注册'''
    if request.method == 'POST':
        phonenum = request.POST.get('phonenum')
        vcode = request.POST.get('vcode')

        key = 'Vcode-%s' % phonenum
        cache_vcode = cache.get(key)

        if vcode and vcode == cache_vcode:
            try:
                user = User.objects.get(phonenum=phonenum)  # 从数据库获取用户
            except User.DoesNotExist:
                # 如果用户不存在，则注册
                user = User.objects.create(phonenum=phonenum, nickname=phonenum)

            # 在session中记录用户登录状态
            request.session['uid'] = user.id

            return JsonResponse({'code': 0, 'data': user.to_dict()})
        else:
            return JsonResponse({'code': 1001, 'data': '验证码错误'})


def show_profile(request):
    '''查看个人资料'''
    uid = request.session['uid']
    profile, _ = Profile.objects.get_or_create(id=uid)
    return JsonResponse({'code': 0, 'data': profile.to_dict()})


def update_profile(request):
    '''更新个人资料'''
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')
        location = request.POST.get('location')
        dating_gender = request.POST.get('dating_gender')
        dating_location = request.POST.get('dating_location')
        max_distance = request.POST.get('max_distance')
        min_distance = request.POST.get('min_distance')
        max_dating_age = request.POST.get('max_dating_age')
        min_dating_age = request.POST.get('min_dating_age')
        vibration = request.POST.get('vibration')
        only_matched = request.POST.get('only_matched')
        auto_play = request.POST.get('auto_play')

        uid = request.session.get('uid')
        user = User.objects.get(pk=uid)
        show = Profile.objects.filter(uid=uid)[0]

        user.nickname = nickname
        user.birthday = birthday
        user.gender = gender
        user.location = location
        user.save()

        show.dating_gender = dating_gender
        show.dating_location = dating_location
        show.max_distance = max_distance
        show.min_distance = min_distance
        show.max_dating_age = max_dating_age
        show.min_dating_age = min_dating_age
        show.vibration = vibration
        show.only_matched = only_matched
        show.auto_play = auto_play
        show.save()

        result = {
            'code': 0,
            'data': 'null',
        }

        return JsonResponse(result)


def qn_token(request):
    '''获取七牛云token'''
    pass


def qn_callback(request):
    '''七牛云回调接口'''
    pass
