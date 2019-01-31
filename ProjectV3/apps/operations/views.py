from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from books.models import Article, Book, BookNotes
from organizations.models import Publisher, Author
from users.models import UserProfile, CarouselBannar
from .models import UserFavorite, ArticleComment, SystemNotefication, BookNotesComment, UserFollow
from .forms import UserAskForm


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                article = Article.objects.get(id=int(fav_id))
                article.favornum -= 1
                if article.favornum < 0:
                    article.favornum = 0
                article.save()
            elif int(fav_type) == 2:
                book = Book.objects.get(id=int(fav_id))
                book.favornum -= 1
                if book.favornum < 0:
                    book.favornum = 0
                book.save()
            elif int(fav_type) == 3:
                publisher = Publisher.objects.get(id=int(fav_id))
                publisher.favnums -= 1
                if publisher.favnums < 0:
                    publisher.favnums = 0
                publisher.save()
            elif int(fav_type) == 4:
                booknotes = BookNotes.objects.get(id=int(fav_id))
                booknotes.favnums -= 1
                if booknotes.favnums < 0:
                    booknotes.favnums = 0
                booknotes.save()
                pass
            elif int(fav_type) == 5:
                author = Author.objects.get(id=int(fav_id))
                author.favnums -= 1
                if author.favnums < 0:
                    author.favnums = 0
                author.save()
                pass
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    article = Article.objects.get(id=int(fav_id))
                    article.favornum += 1
                    article.save()
                elif int(fav_type) == 2:
                    book = Book.objects.get(id=int(fav_id))
                    book.favornum += 1
                    book.save()
                elif int(fav_type) == 3:
                    publisher = Publisher.objects.get(id=int(fav_id))
                    publisher.favnums += 1
                    publisher.save()
                elif int(fav_type) == 4:
                    booknotes = BookNotes.objects.get(id=int(fav_id))
                    booknotes.favornum += 1
                    booknotes.save()
                elif int(fav_type) == 5:
                    author = Author.objects.filter(id=int(fav_id))
                    author.update(favnums=F('favnums') + 1)
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class UserAskView(View):
    def post(self, request):
        form = UserAskForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"你的咨询信息提交失败！"}', content_type='application/json')
        # return redirect('orgs:publisher-detail', pk=request.POST.get('publisher_pk'))


class UserCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        cmmt_type = request.POST.get('cmmt_type', '')
        if cmmt_type == 'article':
            article_id = request.POST.get('article_id', '')
            comments = request.POST.get('comments', '')
            if int(article_id) > 0 and len(comments) > 0:
                artcmmt = ArticleComment(user=request.user, article_id=int(article_id), comments=comments)
                artcmmt.save()
                articles = get_object_or_404(Article, pk=int(article_id))
                articles.commtnum = F('commtnum') + 1
                articles.save()
                articles.refresh_from_db()
                return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"评论出错"}', content_type='application/json')
        elif cmmt_type == 'notes':
            notes_id = request.POST.get('notes_id', '')
            comments = request.POST.get('comments', '')
            if int(notes_id) > 0 and len(comments) > 0:
                notescmmt = BookNotesComment(user=request.user, booknotes_id=int(notes_id), comments=comments)
                notescmmt.save()
                booknotes = BookNotes.objects.filter(id=int(notes_id))
                booknotes.update(commtnum=F('commtnum') + 1)
                # 通知该读书笔记的所有者用户
                notefication = '{0}评论了你的笔记《{1}》:{2}'.format(
                    request.user.nickname, notescmmt.booknotes.title, notescmmt.comments)
                sysy_note = SystemNotefication(user=request.user.id, notefication=notefication, has_read=False)
                sysy_note.save()
                return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"评论出错"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论出错"}', content_type='application/json')


class UserFollowView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        followed = request.POST.get('followed', 0)
        follower = request.user
        exist_records = UserFollow.objects.filter(followed=int(followed), follower=int(follower.id))
        if exist_records:
            # 如果记录已经存在， 则表示当前登陆用户取消关注
            exist_records.delete()
            follower.followed_num -= 1
            if follower.followed_num < 0:
                follower.followed_num = 0
            follower.save()
            followed_user = UserProfile.objects.get(id=int(followed))
            followed_user.follower_num -= 1
            if followed_user.follower_num < 0:
                followed_user.follower_num = 0
            followed_user.save()
            return HttpResponse('{"status":"success", "msg":"关注"}', content_type='application/json')
        else:
            follow = UserFollow()
            follow.follower = follower.id
            follow.followed = int(followed)
            follow.save()
            follower.followed_num += 1
            follower.save()
            followed_user = UserProfile.objects.get(id=int(followed))
            followed_user.follower_num += 1
            followed_user.save()
            return HttpResponse('{"status":"success", "msg":"已关注"}', content_type='application/json')


class IndexView(View):
    def get(self, request):
        recmmd_authors = Author.objects.order_by('-clicknums')[:6]
        recmmd_books = Book.objects.filter(privacy='public', recommend='yes').order_by('-readernum')[:4]
        recmmd_notes = BookNotes.objects.filter(privacy='public').order_by('-clicknum')[:5]
        recmmd_publishers = Publisher.objects.order_by('-clicknums').order_by('-favnums')[:4]
        recmmd_readers = UserProfile.objects.order_by('-follower_num')[:6]
        lunbotus = CarouselBannar.objects.filter(which_page='index')
        return render(request, 'index.html', {
            'recmmd_authors': recmmd_authors, 'recmmd_books': recmmd_books, 'recmmd_notes': recmmd_notes,
            'recmmd_publishers': recmmd_publishers, 'recmmd_readers': recmmd_readers,
            'lunbotus': lunbotus})
