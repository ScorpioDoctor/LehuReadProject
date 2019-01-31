import xadmin
from .models import UserAsk, UserFavorite, UserFollow, ArticleComment, \
    UserMessage, SystemNotefication, UserVisit, BookNotesComment


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'bookname', 'addtime']
    list_filter = ['addtime']
    search_fields = ['name', 'bookname', ]


class UserFavouriteAdmin(object):
    list_display = ['fav_id', 'fav_type', 'user']
    list_filter = ['fav_type', 'user']
    search_fields = ['fav_id', ]


class UserVisitAdmin(object):
    list_display = ['visit_id', 'visit_type', 'visit_count', 'user']
    list_filter = ['visit_type', 'visit_count', 'user']
    search_fields = ['visit_id', ]


class UserFollowAdmin(object):
    list_display = ['followed', 'follower', 'addtime']
    list_filter = ['followed', 'follower', 'addtime']
    search_fields = ['followed', 'follower', ]


class ArticleCommentAdmin(object):
    list_display = ['user', 'article', 'comments', 'addtime']
    list_filter = ['user', 'article', 'addtime']
    search_fields = ['comments', ]


class BookNotesCommentAdmin(object):
    list_display = ['user', 'booknotes', 'comments', 'addtime']
    list_filter = ['user', 'booknotes', 'addtime']
    search_fields = ['comments', ]


class UserMessageAdmin(object):
    list_display = ['from_user', 'to_user', 'message', 'has_read', 'addtime']
    list_filter = ['from_user', 'to_user', 'has_read', 'addtime']
    search_fields = ['message', ]


class SystemNoteficationAdmin(object):
    list_display = ['user', 'notefication', 'has_read', 'addtime']
    list_filter = ['user', 'notefication', 'has_read', 'addtime']
    search_fields = ['notefication', ]


xadmin.sites.site.register(UserAsk, UserAskAdmin)
xadmin.sites.site.register(UserFavorite, UserFavouriteAdmin)
xadmin.sites.site.register(UserVisit, UserVisitAdmin)
xadmin.sites.site.register(UserFollow, UserFollowAdmin)
xadmin.sites.site.register(ArticleComment, ArticleCommentAdmin)
xadmin.sites.site.register(BookNotesComment, BookNotesCommentAdmin)
xadmin.sites.site.register(UserMessage, UserMessageAdmin)
xadmin.sites.site.register(SystemNotefication, SystemNoteficationAdmin)
