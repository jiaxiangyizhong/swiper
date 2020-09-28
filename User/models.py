import datetime

from django.db import models

# Create your models here.
from vip.models import Vip


class User(models.Model):
    GENDERS = (
        ('male', '男性'),
        ('female', '女性'),
    )
    LOCATIONS = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('深圳', '深圳'),
        ('成都', '成都'),
        ('西安', '西安'),
        ('武汉', '武汉'),
        ('沈阳', '沈阳'),
    )
    phonenum = models.CharField(max_length=16, verbose_name='手机号', unique=True)
    nickname = models.CharField(max_length=32, verbose_name='昵称', db_index=True)
    gender = models.CharField(max_length=8, choices=GENDERS, default='male', verbose_name='性别')
    birthday = models.DateField(default='2002-01-01', verbose_name='出生日')
    avatar = models.CharField(default='', max_length=256, verbose_name='个人形象')
    location = models.CharField(default='北京', max_length=16, choices=LOCATIONS, verbose_name='常居地')

    vip_id = models.IntegerField(verbose_name='用户对应的VIP的ID', default=1)
    vip_expire = models.DateTimeField(default='3000-12-31', verbose_name='VIP过期时间')

    class Meta:
        db_table = 'user'

    @property
    def profile(self):
        '''当前用户对应的profile'''
        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    @property
    def vip(self):
        '''当前用户对应的vip'''
        # 检查当前会员是否过期
        now = datetime.datetime.now()
        if now >= self.vip_expire:
            self.set_vip(1)  # 过期时间后强制设置成非会员

        if not hasattr(self, '_vip'):
            self._vip = Vip.objects.get(id=self.vip_id)
        return self._vip

    def set_vip(self, vip_id):
        '''设置当前用户的vip'''
        vip = Vip.objects.get(id=vip_id)
        self.vip_id = vip_id
        self.vip_expire = datetime.datetime.now() + datetime.timedelta(vip.duration)
        self._vip = vip
        self.save()

    def to_dict(self):
        return {
            'id': self.id,
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'gender': self.gender,
            'birthday': str(self.birthday),
            'avatar': self.avatar,
            'location': self.location
        }


class Profile(models.Model):
    dating_gender = models.CharField(max_length=8, default='female',
                                     choices=User.GENDERS, verbose_name='匹配的性别')
    dating_location = models.CharField(max_length=16, default='北京',
                                       choices=User.LOCATIONS, verbose_name='目标城市')
    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=50, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')
    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matched = models.BooleanField(default=True, verbose_name='不让陌生人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')

    class Meta:
        db_table = 'profile'

    def to_dict(self):
        return {
            'id': self.id,
            'dating_gender': self.dating_gender,
            'dating_location': self.dating_location,
            'max_distance': self.max_distance,
            'min_distance': self.min_distance,
            'max_dating_age': self.max_dating_age,
            'min_dating_age': self.min_dating_age,
            'vibration': self.vibration,
            'only_matched': self.only_matched,
            'auto_play': self.auto_play,
        }
