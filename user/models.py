from django.db import models
from django.contrib.auth.models import AbstractUser
class MyUser(AbstractUser):
    qq = models.CharField('QQ号码', max_length=20)
    weChat = models.CharField('微信账号', max_length=20)
    mobile = models.CharField('手机号码', max_length=11, unique=True)
    vip = models.CharField('会员', max_length=6, default=0)
    # 设置返回值
    def __str__(self):
        return self.username

