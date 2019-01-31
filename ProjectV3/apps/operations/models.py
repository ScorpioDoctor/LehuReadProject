from datetime import datetime

from django.db import models

from books.models import Article, Book, BookNotes
from organizations.models import Publisher
from users.models import UserProfile


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    bookname = models.CharField(max_length=50, verbose_name="图书名")
    publisher = models.IntegerField(default=1, verbose_name='出版机构')
    addtime = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name


class ArticleComment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name="文章", on_delete=models.CASCADE)
    comments = models.TextField(verbose_name="评论")
    addtime = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name = "文章评论"
        verbose_name_plural = verbose_name


class BookNotesComment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    booknotes = models.ForeignKey(BookNotes, verbose_name="笔记", on_delete=models.CASCADE)
    comments = models.TextField(verbose_name="评论")
    addtime = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.notes.title

    class Meta:
        verbose_name = "笔记评论"
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    fav_id = models.IntegerField(default=0, verbose_name="数据id")
    fav_type = models.IntegerField(choices=((1, "文章"), (2, "图书"), (3, "出版社"), (4, "笔记"), (5, "作家")),
                                   default=1, verbose_name="收藏类型")
    addtime = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    #
    # def __str__(self):
    #     return self.addtime

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name


class UserVisit(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="访问用户", on_delete=models.CASCADE)
    visit_id = models.IntegerField(default=0, verbose_name="被访问的数据id")
    visit_type = models.IntegerField(choices=((1, "文章"), (2, "图书"), (3, "出版社"), (4, "读者/用户")), default=1,
                                     verbose_name="访问类型")
    visit_count = models.IntegerField(default=0, verbose_name="访问的次数")
    addtime = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户访问"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    from_user = models.ForeignKey(UserProfile, verbose_name='发送者', related_name='from_users', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, verbose_name='接受者', related_name='to_users', on_delete=models.CASCADE)
    message = models.TextField(verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    addtime = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.from_user.username

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name


class SystemNotefication(models.Model):
    user = models.IntegerField(default=0, verbose_name='接受者')
    notefication = models.TextField(verbose_name="通知内容")
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    addtime = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = "系统通知"
        verbose_name_plural = verbose_name


class UserFollow(models.Model):
    followed = models.IntegerField(verbose_name='被关注者', default=-1)
    follower = models.IntegerField(verbose_name='关注者', default=-1)
    addtime = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return str(self.follower)

    class Meta:
        verbose_name = "用户关注"
        verbose_name_plural = verbose_name
