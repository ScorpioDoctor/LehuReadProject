import xadmin

from .models import Category, Tag, Book, Chapter, Article, BookResource, Epoch, LanguageKind, BookNotes, BannerBook


# @xadmin.sites.site.register(Category)
class CategoryAdmin(object):
    list_display = ['catname', 'addtime']
    model_icon = 'fa fa-flag'


# @xadmin.sites.site.register(Tag)
class TagAdmin(object):
    list_display = ['tagname', 'addtime']
    model_icon = 'fa fa-tag'


# @xadmin.site.register(Epoch)
class EpochAdmin(object):
    list_display = ['epochname', 'addtime']
    model_icon = 'fa fa-clock-o'


# @xadmin.site.register(LanguageKind)
class LanguageKindAdmin(object):
    list_display = ['langname', 'addtime']
    model_icon = 'fa fa-file-text-o'


class ChapterInline(object):
    model = Chapter
    extra = 0


class BookResourceInline(object):
    model = BookResource
    extra = 0


# @xadmin.sites.site.register(Book)
class BookAdmin(object):
    list_display = ['title', 'category', 'author', 'wordcount', 'get_chapter_num', 'degree', 'privacy', 'recommend',
                    'readernum', 'clicknum', 'favornum', 'go_to']
    list_filter = ['category', 'wordcount', 'degree', 'privacy', 'recommend', 'readernum', 'clicknum', 'favornum',
                   'addtime']
    list_editable = ['category', 'degree', 'privacy', 'recommend', ]
    search_fields = ['title', 'desc']
    style_fields = {'desc': 'ueditor'}
    model_icon = 'fa fa-book'
    ordering = ['-addtime']
    readonly_fields = ['favornum', 'readernum', ]
    exclude = ['clicknum', ]
    inlines = [ChapterInline, BookResourceInline]
    refresh_times = [50,100]

    def queryset(self):
        qs = super(BookAdmin, self).queryset()
        qs.filter(is_banner=False)
        return qs


class ChapterAdmin(object):
    list_display = ['title', 'wordcount', 'book', 'addtime']
    list_filter = ['wordcount', 'book', 'addtime']
    search_fields = ['title']
    model_icon = 'fa fa-bookmark'
    ordering = ['-addtime']


# @xadmin.sites.site.register(Article)
class ArticleAdmin(object):
    list_display = ['title', 'chapter', 'wordcount', 'clicknum', 'favornum', 'commtnum']
    list_filter = ['chapter', 'wordcount', 'clicknum', 'favornum', 'commtnum', 'addtime']
    search_fields = ['title', 'abstract', 'content']
    model_icon = 'fa fa-file'
    ordering = ['-addtime']
    style_fields = {'content': 'ueditor'}

class BookResourceAdmin(object):
    list_display = ['book', 'name', 'download', 'addtime']
    list_filter = ['book', 'addtime']
    search_fields = ['name']
    model_icon = 'fa fa-folder'
    ordering = ['addtime']


class BookNotesAdmin(object):
    list_display = ['title', 'user', 'book', 'category', 'privacy',
                    'commtnum', 'favornum', 'clicknum', 'addtime']
    list_filter = ['user', 'category', 'privacy', 'addtime']
    search_fields = ['title', 'abstract', 'notes']
    model_icon = 'fa fa-file-text-o'
    ordering = ['-addtime']


class BannerBookAdmin(object):
    list_display = ['title', 'category', 'author', 'wordcount', 'degree', 'privacy', 'recommend', 'readernum',
                    'clicknum', 'favornum']
    list_filter = ['category', 'wordcount', 'degree', 'privacy', 'recommend', 'readernum', 'clicknum', 'favornum',
                   'addtime']
    search_fields = ['title', 'desc']
    style_fields = {'desc': 'ueditor'}
    model_icon = 'fa fa-book'
    ordering = ['-addtime']
    readonly_fields = ['favornum', 'readernum', ]
    exclude = ['clicknum', ]
    inlines = [ChapterInline, BookResourceInline]

    def queryset(self):
        qs = super(BannerBookAdmin, self).queryset()
        qs.filter(is_banner=True)
        return qs


xadmin.site.register(Epoch, EpochAdmin)
xadmin.site.register(LanguageKind, LanguageKindAdmin)
xadmin.sites.site.register(Category, CategoryAdmin)
xadmin.sites.site.register(Tag, TagAdmin)
xadmin.site.register(Book, BookAdmin)
xadmin.site.register(BannerBook, BannerBookAdmin)
xadmin.sites.site.register(Chapter, ChapterAdmin)
xadmin.sites.site.register(Article, ArticleAdmin)
xadmin.sites.site.register(BookResource, BookResourceAdmin)
xadmin.sites.site.register(BookNotes, BookNotesAdmin)
