import xadmin
from xadmin.views import BaseAdminView, CommAdminView
from .models import UserProfile, EmailVerifyRecord, CarouselBannar


@xadmin.sites.register(BaseAdminView)
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


@xadmin.sites.register(CommAdminView)
class GlobalSettings(object):
    site_title = "Xadmin后台管理系统"
    site_footer = "www.studyai.com"
    menu_style = "accordion"


# @xadmin.sites.register(UserProfile)
class UserProfileAdmin(object):
    pass


# @xadmin.sites.register(EmailVerifyRecord)
class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-envelope'

# @xadmin.sites.site.register(CarouselBannar)
class CarouselBannarAdmin(object):
    list_display = ['title', 'info', 'url', 'image']
    search_fields = ['title', 'info', 'url']
    list_filter = ['title', 'info', ]
    model_icon = 'fa fa-picture-o'

xadmin.sites.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)

xadmin.sites.site.register(CarouselBannar, CarouselBannarAdmin)
