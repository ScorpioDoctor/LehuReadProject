from datetime import datetime

from django.db import models

from DjangoUeditor.models import UEditorField


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市")
    desc = models.CharField(max_length=200, verbose_name="描述")
    addtime = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Publisher(models.Model):
    Categories = [('gy', '国有'), ('sy', '私有'), ('hz', '合资'), ('dz', '独资'), ('gfz', '股份制')]
    name = models.CharField(max_length=50, verbose_name='出版社名字')
    category = models.CharField(verbose_name='机构类型', choices=Categories, max_length=3, default='gy')
    abstract = models.CharField(verbose_name='机构简介', max_length=150, default='该机构很赖，没有写简介信息', blank=True)
    # desc = models.TextField(verbose_name='出版社介绍')
    desc = UEditorField(verbose_name='出版社介绍	', width=800, height=500, toolbars="full",
                        imagePath="books/ueditor/", filePath="publisher/ueditor/", blank=True, default="")
    clicknums = models.IntegerField(default=0, verbose_name="点击数")
    favnums = models.IntegerField(default=0, verbose_name="收藏数")
    starnums = models.IntegerField(default=0, verbose_name="星级数")
    image = models.ImageField(upload_to="publisher/%Y/%m", blank=True, null=True,
                              verbose_name="出版社标志", max_length=100)
    address = models.CharField(max_length=150, verbose_name="出版社地址")
    city = models.ForeignKey(CityDict, verbose_name="所在城市", null=True, on_delete=models.SET_NULL)
    addtime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    def get_book_count(self):
        bookcount = 0
        for author in self.author_set.all():
            bookcount += author.book_set.count()
        return bookcount

    class Meta:
        verbose_name = '出版社'
        verbose_name_plural = verbose_name


class Author(models.Model):
    publisher = models.ForeignKey(Publisher, verbose_name='签约出版社', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=25, verbose_name='作者名字')
    workyears = models.IntegerField(default=0, verbose_name="写作年限")
    features = models.CharField(max_length=50, verbose_name="写作风格")
    clicknums = models.IntegerField(default=0, verbose_name="点击数")
    favnums = models.IntegerField(default=0, verbose_name="收藏数")
    age = models.IntegerField(default=18, verbose_name="年龄")
    image = models.ImageField(default='', upload_to="author/%Y/%m", verbose_name="头像", max_length=256)
    addtime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '作者'
        verbose_name_plural = verbose_name
