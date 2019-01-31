import xadmin

from .models import CityDict, Author, Publisher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'addtime']
    list_filter = ['addtime']
    search_fields = ['name', 'desc']


# @xadmin.sites.site.register(Publisher)
class PublisherAdmin(object):
    list_display = ['name', 'city', 'category', 'clicknums', 'favnums', 'address', 'addtime']
    list_filter = ['clicknums', 'favnums', 'city', 'category', 'addtime']
    search_fields = ['name', 'abstract', 'desc']
    style_fields = {'desc': 'ueditor'}


# @xadmin.sites.site.register(Author)
class AuthorAdmin(object):
    list_display = ['name', 'publisher', 'workyears', 'features', 'clicknums', 'favnums',
                    'age', 'addtime']
    list_filter = ['workyears', 'clicknums', 'favnums', 'age', 'addtime']
    search_fields = ['name', 'features']
    relfield_style = 'fk-ajax'


xadmin.sites.site.register(CityDict, CityDictAdmin)
xadmin.sites.site.register(Author, AuthorAdmin)
xadmin.sites.site.register(Publisher, PublisherAdmin)
