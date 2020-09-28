'''程序逻辑配置，以及第三方平台配置'''

# Redis配置
REDIS = {
    'host': 'localhost',
    'port': '6379',
    'db': 2,
}

# 赛迪云通信配置
SD_APPID = '54727'
SD_APPKEY = '0a6aed15afd9b28687c9d21da6607f16'
SD_PROJECT = 'MuUHI2',  # 短信模板的 ID
SD_SIGN_TYPE = 'md5',
SD_API = 'https://api.mysubmail.com/message/xsend.json'

# 七牛云配置
# QN_DOMAIN = 'qh5gmsna6.hb-bkt.clouddn.com'
# QN_BUCKET = 'ezio1'
# QN_ACCESS_KEY = 'xsygLBq55P1qGpGnteqO9kjM6eUKUTG7oGMQlYcT'
# QN_SECRET_KEY = '5Ekpg-LHgvbzG965iKfEo2-4711j_laluXSJHjrJ'
# QN_CALLBACK_URL = 'http://101.200.73.123/qiniu/callback'
# QN_CALLBACK_DOMAIN = '101.200.73.123'


QN_DOMAIN = 'qh5gajv2t.hd-bkt.clouddn.com'
QN_BUCKET = 'shpy'
QN_ACCESS_KEY = 'kEM0sRR-meB92XU43_a6xZqhiyyTuu5yreGCbFtw'
QN_SECRET_KEY = 'QxTKqgnOb_UVldphU261qu9IdzmjkgGHh6GQVPPy'
QN_CALLBACK_URL = 'http://demo.seamile.cn/qiniu/callback'
QN_CALLBACK_DOMAIN = 'demo.seamile.cn'

# 反悔功能相关配置
REWIND_TIMES = 3  # 每日反悔最大次数
REWIND_TIMEOUT = 5 * 60  # 反悔超时时间
