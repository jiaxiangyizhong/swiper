from django.core.cache import cache
from django.http import JsonResponse
from User.logic import send_vcode
from User.models import User, Show


def fetch_vcode(request):
    '''给用户发送验证码'''
    phonenum = request.GET.get('phonenum')
    if send_vcode(phonenum):
        return JsonResponse({'code': 0, 'data': None})
    return JsonResponse({'code': 1000, 'data': None})


def submit_vcode(request):
    '''提交验证码，执行登录注册'''
    if request.method == 'POST':
        phonenum = request.POST.get('phonenum')
        vcode = cache.get(phonenum)
        print(vcode)
        code = request.POST.get('vcode')

        if code != vcode:
            result = {
                'code': 1001,
                'data': 'null'
            }
            return JsonResponse(result)

        users = User.objects.all()
        for user in users:
            if user.phonenum == phonenum:
                result = {
                    'code': 0,
                    'data': {
                        'id': user.id,
                        'nickname': user.nickname,
                        'phonenum': user.phonenum,
                        'birthday': user.birthday,
                        'gender': user.gender,
                        'location': user.location,
                    }
                }
                request.session['uid'] = result['data']['id']
                print(result['data']['id'])
                return JsonResponse(result)
        user = User.objects.create(phonenum=phonenum, nickname=phonenum)
        result = {
            'code': 0,
            'data': {
                'id': user.id,
                'nickname': user.nickname,
                'phonenum': user.phonenum,
                'birthday': user.birthday,
                'gender': user.gender,
                'location': user.location,
            }
        }
        request.session['uid'] = result['data']['id']
        print(result['data']['id'])
        return JsonResponse(result)


def show_profile(request):
    '''查看个人资料'''
    uid = request.session.get('uid')
    shows = Show.objects.all()
    for show in shows:
        if show.uid == uid:
            result = {
                'code': 0,
                'data': {
                    'id': show.uid,
                    'dating_gender': show.dating_gender,
                    'dating_location': show.dating_location,
                    'max_distance': show.max_distance,
                    'min_distance': show.min_distance,
                    'max_dating_age': show.max_dating_age,
                    'min_dating_age': show.min_dating_age,
                    'vibration': show.vibration,
                    'only_matched': show.only_matched,
                    'auto_play': show.auto_play,
                }
            }
            return JsonResponse(result)

    show = Show.objects.create(uid=uid)
    result = {
        'code': 0,
        'data': {
            'id': show.uid,
            'dating_gender': show.dating_gender,
            'dating_location': show.dating_location,
            'max_distance': show.max_distance,
            'min_distance': show.min_distance,
            'max_dating_age': show.max_dating_age,
            'min_dating_age': show.min_dating_age,
            'vibration': show.vibration,
            'only_matched': show.only_matched,
            'auto_play': show.auto_play,
        }
    }
    return JsonResponse(result)


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
        show = Show.objects.filter(uid=uid)[0]

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
