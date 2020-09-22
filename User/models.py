from django.db import models


# Create your models here.
class User(models.Model):
    nickname = models.CharField(max_length=16)
    phonenum = models.CharField(max_length=11)
    birthday = models.DateField(default='2000-01-01')
    gender = models.CharField(max_length=8, choices=(('male', '男'), ('female', '女')), default='male')
    location = models.CharField(default='北京', max_length=16)

    class Meta:
        db_table = 'user'


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
