from django.db import models

# Create your models here.
from django.db.models import Q

from common import errors


class Swiped(models.Model):
    '''滑动记录表'''
    STYPES = (
        ('like', '喜欢'),
        ('superlike', '超级喜欢'),
        ('dislike', '不喜欢'),
    )
    uid = models.IntegerField(verbose_name='滑动者的ID')
    sid = models.IntegerField(verbose_name='被滑动者的ID')
    stype = models.CharField(max_length=10, choices=STYPES, verbose_name='滑动类型')
    stime = models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')

    class Meta:
        unique_together = ['uid', 'sid']
        db_table = 'swiped'

    @classmethod
    def swipe(cls, uid, sid, stype):
        try:
            cls.objects.create(uid=uid, sid=sid, stype=stype)
        except InterruptedError:
            # 抛出重复滑动异常
            raise errors.RepeatSwipeErr

    @classmethod
    def is_liked(cls, uid, sid):
        '''检查是否喜欢过某人'''
        swiped = Swiped.objects.filter(uid=uid, sid=sid).first()
        if not swiped:
            return None  # 喜欢或超级喜欢的用户尚未滑到你
        elif swiped.stype in ['like', 'superlike']:
            return True  # 喜欢或超级喜欢的用户喜欢或超级喜欢你
        else:
            return False  # 喜欢或超级喜欢的用户不喜欢你


class Friend(models.Model):
    '''好友关系表'''
    uid1 = models.IntegerField(verbose_name='UID1')
    uid2 = models.IntegerField(verbose_name='UID2')

    class Meta:
        unique_together = ['uid1', 'uid2']
        db_table = 'friend'

    @classmethod
    def make_friends(cls, uid1, uid2):
        '''创建好友关系'''
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)  # 调整两者位置
        return cls.objects.create(uid1=uid1, uid2=uid2)

    @classmethod
    def breakoff(cls, uid1, uid2):
        '''删除好友关系'''
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)  # 调整两者位置
        cls.objects.filter(uid1=uid1, uid2=uid2).delete()

    @classmethod
    def friend_ids(cls, uid):
        '''查找自己的所有好友ID'''
        uid_list = []
        condition = Q(uid1=uid) | Q(uid2=uid)
        for frd in cls.objects.filter(condition):
            if frd.uid1 == uid:
                uid_list.append(frd.uid2)
            else:
                uid_list.append(frd.uid1)

        return uid_list
