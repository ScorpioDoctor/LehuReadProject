# _*_ coding: utf-8 _*_

from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=20, null=True, blank=True, verbose_name='昵称')
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(choices=(("male", "男"), ("female", "女")), default="female",
                              max_length=6, verbose_name='性别')
    address = models.CharField(max_length=100, default="", verbose_name='地址', null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    image = models.ImageField(upload_to="image/%Y/%m", null=True, blank=True,
                              default="image/default.png", max_length=100, verbose_name='头像')
    followed_num = models.IntegerField(default=0, verbose_name='我关注的数量')
    follower_num = models.IntegerField(default=0, verbose_name='关注我的数量')

    def __str__(self):
        return self.username

    def get_messages_count(self):
        from operations.models import UserMessage, SystemNotefication
        usermessages = UserMessage.objects.filter(to_user=self, has_read=False)
        sysmessages = SystemNotefication.objects.filter(user=self.pk, has_read=False)
        return usermessages.count() + sysmessages.count()

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(choices=(("register", "注册"), ("forget", "找回密码")),
                                 max_length=15, verbose_name="验证码类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name


class CarouselBannar(models.Model):
    which_page = models.CharField(
        choices=(('index', '首页'), ('login', '登录页面'), ('regist', '注册页面'), ('forgetpwd', '密码找回页面')),
        max_length=20, default='index')
    title = models.CharField(max_length=20, verbose_name='轮播标题', blank=True, null=True)
    info = models.CharField(max_length=50, verbose_name='轮播信息', blank=True, null=True)
    url = models.CharField(max_length=120, verbose_name='轮播链接', blank=True, null=True)
    image = models.ImageField(upload_to="image/%Y/%m", null=True, blank=True,
                              default="image/default.png", max_length=100, verbose_name='轮播图片')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name
