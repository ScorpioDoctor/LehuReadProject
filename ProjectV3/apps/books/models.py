# _*_ coding: utf-8 _*_
from datetime import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Sum

from DjangoUeditor.models import UEditorField
from django.db import models
from organizations.models import Author
from users.models import UserProfile


class Category(models.Model):
    catname = models.CharField(max_length=25, verbose_name='类别名称')
    addtime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.catname

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    tagname = models.CharField(max_length=25, verbose_name='标签名称')
    addtime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.tagname

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class LanguageKind(models.Model):
    langname = models.CharField(max_length=25, verbose_name='语言名称')
    addtime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.langname

    class Meta:
        verbose_name = '语种'
        verbose_name_plural = verbose_name


class Epoch(models.Model):
    epochname = models.CharField(max_length=25, verbose_name='时代名称')
    addtime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.epochname

    class Meta:
        verbose_name = '时代'
        verbose_name_plural = verbose_name


class Book(models.Model):
    category = models.ForeignKey(Category, verbose_name="类别", null=True, blank=True, on_delete=models.SET_NULL)
    epoch = models.ForeignKey(Epoch, verbose_name="时代", null=True, blank=True, on_delete=models.SET_NULL)
    languagekind = models.ForeignKey(LanguageKind, verbose_name="语种", null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="标签")
    author = models.ForeignKey(Author, verbose_name='作者', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='图书名称')
    wordcount = models.IntegerField(verbose_name='总字数', default=0, null=True)
    starnums = models.IntegerField(verbose_name='星级', default=0)
    degree = models.CharField(verbose_name="难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)
    abstract = models.CharField(max_length=150, verbose_name='图书简介', default='这本书没有简介', blank=True)
    # desc = models.TextField(verbose_name='图书描述',default='')
    desc = UEditorField(verbose_name='图书描述	', width=800, height=500, toolbars="full",
                        imagePath="books/ueditor/", filePath="books/ueditor/", blank=True, default="")
    cover = models.ImageField(upload_to='books/%Y/%m/', verbose_name='图书封面', max_length=255, null=True, blank=True)
    privacy = models.CharField(verbose_name="权限", choices=(("private", "私密"), ("public", "公开")), max_length=8)
    recommend = models.CharField(verbose_name='推荐', choices=(("yes", "推荐到首页"), ("no", "不推荐到首页")), max_length=4)
    readernum = models.IntegerField(verbose_name='读者人数', default=0)
    clicknum = models.IntegerField(verbose_name='点击量', default=0)
    favornum = models.IntegerField(verbose_name='收藏量', default=0)
    is_banner = models.BooleanField(verbose_name='是否轮播课程', default=False)
    addtime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.title

    def get_chapter_num(self):
        return self.chapter_set.count()

    get_chapter_num.short_description = '章节数'

    def get_book_wordcount(self):
        # 使用聚合函数计算该书的总字数
        book_wordcount = self.chapter_set.aggregate(WordCount=Sum('wordcount'))
        self.wordcount = book_wordcount.get('WordCount')
        self.save()
        return self.wordcount

    get_book_wordcount.short_description = '总字数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http:www.studyai.com'>查看</a>")

    go_to.short_description = '跳转'

    class Meta:
        verbose_name = '图书'
        verbose_name_plural = verbose_name


class Chapter(models.Model):
    title = models.CharField(max_length=255, verbose_name='章节标题')
    wordcount = models.IntegerField(verbose_name='章节字数', default=0, null=True)
    book = models.ForeignKey(Book, verbose_name="所属图书", on_delete=models.CASCADE)
    addtime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.title

    def get_chapter_wordcount(self):
        # 使用聚合函数计算该章节的总字数
        chapter_wordcount = self.article_set.aggregate(WordCount=Sum('wordcount'))
        self.wordcount = chapter_wordcount.get('WordCount')
        self.save()
        return self.wordcount

    get_chapter_wordcount.short_description = '章节总字数'

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name


class Article(models.Model):
    chapter = models.ForeignKey(Chapter, verbose_name="所属章节", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='文章标题')
    abstract = models.CharField(max_length=120, verbose_name='文章摘要', default='这篇文章没有摘要', blank=True)
    cover = models.ImageField(upload_to='articles/%Y/%m/', verbose_name='文章封面', max_length=255, null=True, blank=True)
    # content = models.TextField(verbose_name='文章内容')
    content = UEditorField(verbose_name='文章内容', width=800, height=500, toolbars="full",
                           imagePath="books/ueditor/", filePath="books/ueditor/", blank=True, default="")
    wordcount = models.IntegerField(verbose_name='文章字数', default=0, null=True)
    clicknum = models.IntegerField(verbose_name='点击量', default=0)
    favornum = models.IntegerField(verbose_name='收藏量', default=0)
    commtnum = models.IntegerField(verbose_name='评论量', default=0)
    addtime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class BookResource(models.Model):
    book = models.ForeignKey(Book, verbose_name="图书", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="名称")
    download = models.FileField(upload_to="books/resources/%Y/%m", verbose_name=u"资源文件", max_length=100)
    addtime = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "图书资源"
        verbose_name_plural = verbose_name


class BookNotes(models.Model):
    """读书笔记"""
    category = models.ForeignKey(Category, verbose_name="类别", null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="标签")
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name="图书", null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=50, verbose_name="笔记标题")
    abstract = models.CharField(max_length=120, verbose_name='笔记摘要')
    # notes = models.TextField(verbose_name="笔记内容")
    # notes = UEditorField(verbose_name='笔记内容	', width=800, height=500, toolbars="full",
    #                      imagePath="notes/ueditor/", filePath="notes/ueditor/", blank=True, default="")
    notes = RichTextUploadingField(verbose_name="笔记内容")
    privacy = models.CharField(verbose_name="权限", choices=(("private", "私密"), ("public", "公开")), max_length=8)
    cover = models.ImageField(upload_to='notes/%Y/%m/', verbose_name='笔记封面', max_length=255, null=True, blank=True)
    clicknum = models.IntegerField(verbose_name='点击量', default=0, blank=True)
    favornum = models.IntegerField(verbose_name='收藏量', default=0, blank=True)
    commtnum = models.IntegerField(verbose_name='评论量', default=0, blank=True)
    addtime = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "阅读笔记"
        verbose_name_plural = verbose_name


class BannerBook(Book):
    class Meta:
        verbose_name = '轮播图书'
        verbose_name_plural = verbose_name
        proxy = True
