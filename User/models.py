from django.db import models


# Create your models here.
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

    class Meta:
        db_table = 'user'

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


class Show(models.Model):
    uid = models.IntegerField()
    dating_gender = models.CharField(max_length=16, default='female')
    dating_location = models.CharField(max_length=16, default='北京')
    max_distance = models.IntegerField(default=10)
    min_distance = models.IntegerField(default=1)
    max_dating_age = models.IntegerField(default=50)
    min_dating_age = models.IntegerField(default=20)
    vibration = models.BooleanField(default=0)
    only_matched = models.BooleanField(default=0)
    auto_play = models.BooleanField(default=0)

    class Meta:
        db_table = 'show'

    def to_dict(self):
        return {
            'uid': self.uid,
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
