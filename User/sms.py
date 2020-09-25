import random
import time
import json
from hashlib import md5

import requests
from django.core.cache import cache


def send_code(phonenum):
    appid = '54727'
    appkey = '0a6aed15afd9b28687c9d21da6607f16'
    vcode = ""
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        vcode += ch

    args = {
        'appid': '54727',  # APPID
        'to': phonenum,  # 手机号
        'project': 'MuUHI2',  # 短信模板的 ID
        'vars': json.dumps({'vcode': vcode}),
        'timestamp': int(time.time()),
        'sign_type': 'md5',
    }

    api = 'https://api.mysubmail.com/message/xsend.json'

    # # 计算参数的签名
    # sorted_args = sorted(args.items())  # 提取每一项
    # args_str = '&'.join([f'{key}={value}' for key, value in sorted_args])  # 对参数排序、组合
    # sign_str = f'{appid}{appkey}{args_str}{appid}{appkey}'.encode('utf8')  # 拼接成待签名字符串
    # signature = md5(sign_str).hexdigest()  # 计算签名
    # args['signature'] = signature

    response = requests.post(api, data=args)
    print('状态码：', response.status_code)

    result = response.json()
    # print('短信结果：', result)

    data = {
        'response': response.status_code,
        'vcode': vcode,
    }

    return data
