import json
import time
from qiniu import Auth
from swiper import config as cfg


def get_res_url(filename):
    # 获取资源的URL
    return f'http://{cfg.QN_DOMAIN}/{filename}'


def gen_token(uid, filename):
    policy = {
        'scope': cfg.QN_BUCKET,
        'deadline': int(time.time() + 600),
        'returnBody': json.dumps({"code": 0, "data": get_res_url}),
        'callbackUrl': cfg.QN_CALLBACK_URL,
        'callbackHost': cfg.QN_CALLBACK_DOMAIN,
        'callbackBody': f'key={filename}&uid={uid}',
        'saveKey': filename,
        'forceSaveKey': True,
        'fsizeLimit': 10485760,  # 文件大小的最大值：10MB
        'mimeLimit': 'image/*',
    }

    # 构建鉴权对象
    qn_auth = Auth(cfg.QN_Access_Key, cfg.QN_Secret_Key)

    # 生成上传 Token，可以指定过期时间等
    token = qn_auth.upload_token(cfg.QN_BUCKET, filename, 600, policy)

    return token
