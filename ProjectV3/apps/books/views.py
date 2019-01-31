from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from books.forms import BookNotesEditForm
from operations.models import UserFavorite, UserVisit
from organizations.models import Author
from .models import Category, Tag, Book, Article, BookNotes


class BookListView(View):
    def get(self, request):
        # 取出所有书
        book_list = Book.objects.all()
        # 按语种过滤
        lang = request.GET.get('lang', '')
        if lang:
            book_list = book_list.filter(languagekind_id=lang)
        # 按年代过滤
        epch = request.GET.get('epch', '')
        if epch:
            book_list = book_list.filter(epoch_id=epch)
        # 按种类过滤
        ctg = request.GET.get('ctg', '')
        if ctg:
            book_list = book_list.filter(category_id=ctg)
        # 按标签过滤
        tag = request.GET.get('tag', '')
        if tag:
            book_list = book_list.filter(tags=tag)
        # 按搜索字段过滤
        schkwds = request.GET.get('schkwds', '')
        if schkwds:
            book_list = book_list.filter(Q(title__icontains=schkwds) |
                                         Q(abstract__icontains=schkwds) |
                                         Q(desc__icontains=schkwds))
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(book_list, 8, request=request)
        book_list = p.page(page)
        return render(request, 'book_list.html', {
            'book_list': book_list, 'lang': lang, 'epch': epch, 'ctg': ctg})


class BookDetailView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        # 记录浏览次数
        book.clicknum += 1
        book.save()
        # 获取当前图书的所有访客
        visitions = UserVisit.objects.filter(visit_id=book.pk, visit_type=2).all()
        # 如果是登录用户，就记录访客
        if request.user.is_authenticated:
            existed_visition = UserVisit.objects.filter(user=request.user, visit_id=book.pk, visit_type=2).first()
            if existed_visition:
                existed_visition.visit_count = F('visit_count') + 1
                existed_visition.save()
            else:
                visition = UserVisit(user=request.user, visit_id=book.pk, visit_type=2, visit_count=1)
                visition.save()
        # 获取该书相关的阅读笔记
        booknotes_list = BookNotes.objects.filter(book=book, privacy='public').order_by('-addtime').all()
        return render(request, 'book_detail.html', {
            'book': book, 'visitions': visitions, 'booknotes_list': booknotes_list})


class ChapterListView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        # 记录阅读次数
        book.readernum = F("readernum") + 1
        book.save()
        book.refresh_from_db()
        has_fav = False
        if request.user.is_authenticated:
            existed = UserFavorite.objects.filter(fav_id=book.id, user=request.user)
            if existed:
                has_fav = True
        # 定位章节位置
        chapter = request.GET.get('ch', '1')
        return render(request, 'book_read.html', {'book': book, 'has_fav': has_fav, 'chapter': chapter})


class ArticleDetailView(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        book = get_object_or_404(Book, pk=article.chapter.book.pk)
        author = book.author
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            existed = UserFavorite.objects.filter(fav_id=article.id, user=request.user)
            if existed:
                has_fav = True
        # 获取当前文章的所有访客
        visitions = UserVisit.objects.filter(visit_id=article.pk, visit_type=1).all()
        # 如果是登录用户，就记录阅读文章的访客
        if request.user.is_authenticated:
            existed_visition = UserVisit.objects.filter(user=request.user, visit_id=article.pk, visit_type=1).first()
            if existed_visition:
                existed_visition.visit_count = F('visit_count') + 1
                existed_visition.save()
            else:
                visition = UserVisit(user=request.user, visit_id=article.pk, visit_type=1, visit_count=1)
                visition.save()
        return render(request, 'article_detail.html', {
            'article': article, 'book': book, 'author': author,
            'has_fav': has_fav, 'visitions': visitions})


class BookNotesListView(View):
    def get(self, request):
        booknotes_list = BookNotes.objects.filter(privacy='public')
        # 按种类过滤
        ctg = request.GET.get('ctg', '')
        if ctg:
            booknotes_list = booknotes_list.filter(category_id=ctg)
        # 按标签过滤
        tag = request.GET.get('tag', '')
        if tag:
            booknotes_list = booknotes_list.filter(tags=tag)
        # 按搜索字段过滤
        schkwds = request.GET.get('schkwds', '')
        if schkwds:
            booknotes_list = booknotes_list.filter(Q(title__icontains=schkwds) |
                                                   Q(abstract__icontains=schkwds) |
                                                   Q(notes__icontains=schkwds))
        # 过滤完之后再排序(效率高)
        order = request.GET.get('order', '')
        if order:
            booknotes_list = booknotes_list.order_by('-' + order)
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(booknotes_list, 3, request=request)
        booknotes_list = p.page(page)
        return render(request, 'booknotes_list.html', {
            'booknotes_list': booknotes_list, 'order': order})


class BookNotesDetailView(View):
    def get(self, request, pk):
        booknotes = get_object_or_404(BookNotes, pk=pk)
        booknotes.clicknum += 1
        booknotes.save()
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            existed = UserFavorite.objects.filter(fav_id=booknotes.id, user=request.user)
            if existed:
                has_fav = True
        return render(request, 'booknotes_detail.html', {'booknotes': booknotes, 'has_fav': has_fav})


class BookNotesArchiveView(View):
    def get(self, request, year, month, day):
        booknotes_list = BookNotes.objects.filter(
            privacy='public', addtime__year=year, addtime__month=month, addtime__day=day)
        # 按种类过滤
        ctg = request.GET.get('ctg', '')
        if ctg:
            booknotes_list = booknotes_list.filter(category_id=ctg)
        # 按标签过滤
        tag = request.GET.get('tag', '')
        if tag:
            booknotes_list = booknotes_list.filter(tags=tag)
        # 过滤完之后再排序(效率高)
        order = request.GET.get('order', '')
        if order:
            booknotes_list = booknotes_list.order_by('-' + order)
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(booknotes_list, 3, request=request)
        booknotes_list = p.page(page)
        return render(request, 'booknotes_list.html', {
            'booknotes_list': booknotes_list, 'order': order})


class BookNotesDeleteView(View):
    def post(self, request):
        notes_id = request.POST.get('notes_id', 0)
        user_id = request.POST.get('user_id', 0)
        exist_records = BookNotes.objects.filter(id=int(notes_id), user_id=int(user_id)).first()
        if exist_records:
            # 如果记录已经存在， 则直接删除
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"删除出错"}', content_type='application/json')


class BookNotesEditView(View):
    def get(self, request, pk):
        notes_instance = BookNotes.objects.get(pk=pk)
        notes_form = BookNotesEditForm()
        return render(request, 'booknotes_edit.html', {
            "notes_form": notes_form, 'notes_instance': notes_instance})

    def post(self, request, pk):
        notes_instance = BookNotes.objects.get(pk=pk)
        notes_form = BookNotesEditForm(data=request.POST, files=request.FILES, instance=notes_instance)
        if notes_form.is_valid():
            notes_form.save()
        return redirect('books:booknotes-detail', pk=notes_form.instance.pk)
