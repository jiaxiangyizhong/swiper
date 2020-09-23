import re
from django.core.cache import cache
from libs.sms import send_sms
import random


def is_phonenum(phonenum):
    '''验证是否是一个正确的手机号'''
    if re.match(r'1[3-9]\d{9}$', phonenum):
        return True
    return False


def random_code(length=6):
    '''产生指定长度随机码'''
    nums = [str(random.randint(0, 9)) for i in range(length)]
    return ''.join(nums)


def send_vcode(phonenum):
    ''' 给用户发送短信验证码 '''

    # 验证手机号
    if not is_phonenum(phonenum):
        return False

    key = 'Vcode-%s' % phonenum
    # 检查缓存中是否已有验证码，防止用户频繁调用接口
    if cache.get(key):
        return True

    # 产生验证码
    vcode = random_code()
    print('随机码：', vcode)
    cache.set('Vcode-%s' % phonenum, vcode, timeout=600)  # 将验证码添加到缓存中，并多设置一些时间

    # 向用户手机发送验证码
    return send_sms(phonenum, vcode)
