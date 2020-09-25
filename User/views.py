from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from User.models import User, Show
from User.sms import send_code


def index(request):
    return HttpResponse('index')


def fetch(request):
    phonenum = request.GET.get('phonenum')
    data = send_code(phonenum)
    vcode = data['vcode']
    print(vcode)
    cache.set(phonenum, vcode, timeout=60*10)

    result = {
        'code': 0,
        'data': 'null'
    }
    if data['response'] == 200:
        return JsonResponse(result)
    result['code'] = 1000
    return JsonResponse(result)


def submit(request):
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


def show(request):
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


def update(request):
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
