"""ProjectV3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import url
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from ProjectV3.settings import MEDIA_ROOT
from operations.views import IndexView

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # 配置上传文件的访问处理函数
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 首页
    path('', IndexView.as_view(), name='index'),
    # 用户相关路由
    path('users/', include('users.urls', namespace='users')),
    # 获取注册验证码
    path('captcha/', include('captcha.urls')),
    # 机构相关的urls
    path('orgs/', include('organizations.urls', namespace='orgs')),
    # 用户操作相关的URL
    path('operates/', include('operations.urls', namespace='operates')),
    # 图书相关的URL
    path('books/', include('books.urls', namespace='books')),
    # Ueditor的url
    re_path(r'^ueditor/', include('DjangoUeditor.urls')),
    # CKEditor的url
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

# 全局404页面配置
handler404 = 'users.views.page_not_found'
