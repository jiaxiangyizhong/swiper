from User.logic import send_vcode
from common import errors
from common import keys
from libs.cache import rds
from libs.http import render_json
from User.models import User, Profile
from User.forms import UserForm, ProfileForm
from libs.qn_cloud import gen_token, get_res_url


def fetch_vcode(request):
    '''给用户发送验证码'''
    phonenum = request.GET.get('phonenum')

    send_vcode.delay(phonenum)  # 异步发送短信验证码
    key = keys.VCODE_K % phonenum
    vcode = rds.get(key)
    print(vcode)
    return render_json()


def submit_vcode(request):
    '''提交验证码，执行登录注册'''
    if request.method == 'POST':
        phonenum = request.POST.get('phonenum')
        vcode = request.POST.get('vcode')

        key = keys.VCODE_K % phonenum
        cache_vcode = rds.get(key)

        if vcode and vcode == cache_vcode:
            try:
                user = User.objects.get(phonenum=phonenum)  # 从数据库获取用户
            except User.DoesNotExist:
                # 如果用户不存在，则注册
                user = User.objects.create(phonenum=phonenum, nickname=phonenum)

            # 在session中记录用户登录状态
            request.session['uid'] = user.id

            return render_json(user.to_dict())
        else:
            return render_json(code=errors.VCODE_ERR, data='验证码错误')


def show_profile(request):
    '''查看个人资料'''
    uid = request.session['uid']
    profile, _ = Profile.objects.get_or_create(id=uid)
    return render_json(profile.to_dict())


def update_profile(request):
    '''更新个人资料'''
    # 定义form对象
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)

    # 检查验证数据
    if user_form.is_valid() and profile_form.is_valid():
        uid = request.session['uid']

        User.objects.filter(id=uid).update(**user_form.cleaned_data)
        Profile.objects.update_or_create(id=uid, defaults=profile_form.cleaned_data)
        return render_json()

    err = {}
    err.update(user_form.errors)
    err.update(profile_form.errors)
    return render_json(data=err, code=errors.PROFILE_ERR)


def qn_token(request):
    '''获取七牛云token'''
    uid = request.session['uid']
    filename = f'Avatar-{uid}'
    token = gen_token(uid, filename)
    return render_json({'token': token, 'key': filename})


def qn_callback(request):
    '''七牛云回调接口'''
    uid = request.POST.get('uid')
    key = request.POST.get('key')
    avatar_url = get_res_url(key)
    User.objects.filter(id=uid).update(avatar=avatar_url)

    return render_json(avatar_url)
