import datetime
from django.db.transaction import atomic
from User.models import User, Profile
from common import keys, errors
from libs.cache import rds
from social.models import Swiped, Friend
from swiper import config


def rcmd_from_queue(uid):
    '''从优先推荐队列进行推荐'''
    uid_list = rds.lrange(keys.FirstRcmdQ % uid, 0, 19)  # 取出优先推荐队列中uid列表
    uid_list = [int(uid) for uid in uid_list]  # 将uid强转成int类型
    return User.objects.filter(id__in=uid_list)


def rcmd_from_db(uid, num=20):
    '''从数据库中推荐滑动用户'''
    profile = Profile.objects.get(id=uid)

    # 计算出生日期范围
    today = datetime.date.today()
    earliest_birth = today - datetime.timedelta(profile.max_dating_age * 365)  # 最早出生日期
    latest_birth = today - datetime.timedelta(profile.min_dating_age * 365)  # 最晚出生日期

    # 获取已经滑过的用户ID
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    users = User.objects.filter(
        location=profile.dating_location,
        gender=profile.dating_gender,
        birthday__range=[earliest_birth, latest_birth],
    ).exclude(id__in=sid_list)[:num]

    return users


def rcmd(uid):
    '''推荐滑动用户'''
    first_users = rcmd_from_queue(uid)
    remain = 20 - len(first_users)  # 计算需要从数据库中获取的个数
    if remain:
        second_users = rcmd_from_db(uid, remain)

        return set(first_users) | set(second_users)
    else:
        return first_users


def like_someone(uid, sid):
    '''喜欢某人（右滑）'''
    # 1. 添加滑动记录
    Swiped.swipe(uid, sid, stype='like')

    # 删除优先推荐队列中的sid
    rds.lrem(keys.FirstRcmdQ % uid, count=0, value=sid)
    # 2. 检查对方是否喜欢（右滑或上滑）过自己
    # 3. 将互相喜欢的两人添加成好友
    if Swiped.is_liked(sid, uid):
        Friend.make_friends(uid, sid)
        return True
    else:
        return False


@atomic
def superlike_someone(uid, sid):
    '''超级喜欢某人（上滑）'''
    # 添加滑动记录
    Swiped.swipe(uid, sid, 'superlike')
    # 删除优先推荐队列中的sid
    rds.lrem(keys.FirstRcmdQ % uid, count=0, value=sid)

    liked = Swiped.is_liked(sid, uid)
    # 将互相喜欢的两人添加成好友
    if liked is True:
        Friend.make_friends(uid, sid)
        return True
    elif liked is False:
        return False
    else:
        # 若对方未滑过自己，将自己优先推荐给对方
        rds.rpush(keys.FirstRcmdQ % sid, uid)
        return False


def dislike_someone(uid, sid):
    '''不喜欢某人（左滑）'''
    Swiped.swipe(uid, sid, 'dislike')
    rds.lrem(keys.FirstRcmdQ % uid, count=0, value=sid)


def rewind_last_swipe(uid):
    '''反悔上一次滑动（每天只允许3次，反悔的记录只能是五分钟之内的）'''
    now = datetime.datetime.now()

    # 检查今天是否已经反悔3次（记录在redis中）
    rewind_key = keys.REWIND_TIMES_K % (now.date(), uid)
    rewind_times = rds.get(rewind_key, 0)
    if rewind_times >= config.REWIND_TIMES:
        raise errors.RewindLimit

    # 找到最后一次滑动
    last_swipe = Swiped.objects.filter(uid=uid).latest('stime')

    # 检查最后一次滑动是否在五分钟以内
    time_past = (now - last_swipe.stime).total_seconds()
    if time_past >= config.REWIND_TIMEOUT:
        raise errors.RewindTimeout

    with atomic():  # 将多次数据修改在事务中执行
        # 如果之前匹配成好友，则删除好友关系
        if last_swipe.stype in ['like', 'superlike']:
            Friend.breakoff(uid, last_swipe.sid)

        # 如果上一次是超级喜欢，则从对方的优先推荐队列中删除自己的uid
        if last_swipe.stype == 'superlike':
            rds.lrem(keys.FirstRcmdQ % last_swipe.sid, 0, uid)

        # 删除最后一次滑动
        last_swipe.delete()

        # 今日反悔次数加一
        rds.set(rewind_key, rewind_times + 1, 86460)  # 缓存过期时间为一天零60秒


def find_my_fans(uid):
    '''查找我的粉丝'''

    # 取出自己滑过的用户
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    # 在所有喜欢自己的人并去除自己已经滑过的人
    fans_id_list = Swiped.objects.filter(sid=uid, stype__in=['like', 'superlike']) \
        .exclude(uid__in=sid_list).values_list('uid', flat=True)

    users = User.objects.filter(id__in=fans_id_list)
    return users
