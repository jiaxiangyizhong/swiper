import json
from django.conf import settings
from django.http import HttpResponse


def render_json(data=None, code=0):
    # 将结果渲染成json数据
    result = {
        'data': data,
        'code': code
    }

    if settings.DEBUG is True:
        json_str = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        json_str = json.dumps(result, ensure_ascii=False, separators=(',', ':'))

    response = HttpResponse(content=json_str, content_type='application/json')
    return response
