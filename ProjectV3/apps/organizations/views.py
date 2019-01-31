from django.db.models import F, Q
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from books.models import Article
from operations.models import UserFavorite, UserVisit
from .models import Publisher, CityDict, Author


class PublisherListView(View):
    def get(self, request):
        city_list = CityDict.objects.all()
        publisher_list = Publisher.objects.all()
        publisher_ranks = publisher_list.order_by('-clicknums')[:6]
        # 按条件过滤
        city = request.GET.get('city', '')
        if city:
            publisher_list = publisher_list.filter(city_id=city)
        cat = request.GET.get('cat', '')
        if cat:
            publisher_list = publisher_list.filter(category=cat)
        # 按搜索字段过滤
        schkwds = request.GET.get('schkwds', '')
        if schkwds:
            publisher_list = publisher_list.filter(Q(name__icontains=schkwds) |
                                                   Q(abstract__icontains=schkwds) |
                                                   Q(desc__icontains=schkwds))
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(publisher_list, 4, request=request)
        publisher_list = p.page(page)
        return render(request, 'publisher_list.html', {
            'cat': cat, 'cid': city, 'publisher_list': publisher_list, 'city_list': city_list,
            'publisher_ranks': publisher_ranks})


class PublisherDetailView(View):
    def get(self, request, pk):
        publisher = Publisher.objects.filter(pk=pk)
        publisher.update(clicknums=F('clicknums') + 1)
        publisher = publisher.first()
        starnums = range(publisher.starnums)
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            existed_favs = UserFavorite.objects.filter(fav_id=publisher.id, user=request.user, fav_type=3)
            if existed_favs is None:
                has_fav = False
            else:
                has_fav = True

        # 获取当前图书的所有访客
        visitions = UserVisit.objects.filter(visit_id=publisher.pk, visit_type=3)
        # 如果是登录用户，就记录访客
        if request.user.is_authenticated:
            existed_visition = UserVisit.objects.filter(
                user=request.user, visit_id=publisher.pk, visit_type=3)
            if existed_visition:
                existed_visition.update(visit_count=F('visit_count') + 1)
                # existed_visition.save()
            else:
                visition = UserVisit(user=request.user, visit_id=publisher.pk, visit_type=3, visit_count=1)
                visition.save()
        return render(request, 'publisher_detail.html', {
            'publisher': publisher, 'starnums': starnums, 'has_fav': has_fav, 'visitions': visitions})


class AuthorDetailView(View):
    def get(self, request, pk):
        # author = get_object_or_404(Author, pk=pk)
        # author.clicknums = F('clicknums') + 1
        # author.save()
        # author.refresh_from_db()
        author = Author.objects.filter(pk=pk)
        author.update(clicknums=F('clicknums') + 1)
        author = author.first()
        newest_articles = Article.objects.filter(chapter__book__author=author).order_by('-addtime')[:5]
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            existed_favs = UserFavorite.objects.filter(fav_id=author.id, user=request.user, fav_type=5).first()
            if existed_favs is not None:
                has_fav = True
        return render(request, 'author_detail.html', {
            'author': author, 'newest_articles': newest_articles, 'has_fav': has_fav})
