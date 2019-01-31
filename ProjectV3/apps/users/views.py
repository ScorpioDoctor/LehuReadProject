import json

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q, F
from django.urls import reverse
from django.views.generic.base import View

from books.models import Article, Book, BookNotes, Category, Tag
from operations.models import UserFavorite, UserMessage, SystemNotefication, UserFollow, UserVisit
from organizations.models import Publisher, Author
from utils.email_send import send_register_email
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegistForm, ForgetForm, ModifyPwdForm, UpdatePwdForm, UpdateUserInfoForm, UploadImageForm, \
    BookNotesForm


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutView(View):
    def get(self, request):
        logout(request)
        # return redirect('index')
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            user_pwd = request.POST.get('password', '')
            user = authenticate(username=user_name, password=user_pwd)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return render(request, "index.html", {})
                    return redirect('index')
                else:
                    return render(request, "login.html", {"msg": "用户帐号未激活！"})
            else:
                return render(request, "login.html", {"msg": "用户名or密码输入错误！"})
        else:
            return render(request, 'login.html', context={'login_form': login_form})


class RegistView(View):
    def get(self, request):
        register_form = RegistForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegistForm(request.POST)
        if register_form.is_valid():
            user_email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_email):
                return render(request, 'register.html', {'msg': '用户邮箱已经存在！', 'register_form': register_form})
            user_pwd = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.email = user_email
            user_profile.username = user_email
            user_profile.nickname = "牛二丹"
            user_profile.password = make_password(user_pwd)
            # 设置用户激活状态:
            user_profile.is_active = False
            user_profile.save()
            # 发送注册邮件
            send_register_email(user_email, 'register')
            return render(request, 'login.html', {})
        else:
            return render(request, 'register.html', {'register_form': register_form})


class AciveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        # return render(request, "login.html")
        return redirect('users:login')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetPwdView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            # return render(request, "login2.html")
            return redirect(to='users:login')
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserCenterView(View):
    def get(self, request):
        msg_dates = UserMessage.objects.filter(to_user=request.user).dates('addtime', 'day', order='DESC')
        return render(request, 'user_center.html', {'msg_dates': msg_dates})

    def post(self, request):
        msg_id = request.POST.get('msg_id', 0)
        from_user_id = request.POST.get('from_user_id', 0)
        exist_records = UserMessage.objects.filter(id=int(msg_id), from_user_id=int(from_user_id),
                                                   to_user_id=int(request.user.id)).first()
        if exist_records:
            # 如果记录已经存在， 则直接删除
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"删除出错"}', content_type='application/json')


class UserCenterGuestView(View):
    def get(self, request, pk):
        user = UserProfile.objects.get(pk=pk)
        has_follow = False
        if request.user.is_authenticated and request.user.id != pk:
            existed = UserFollow.objects.filter(followed=pk, follower=request.user.id)
            if existed:
                has_follow = True
        # 获取当前用户的所有访客
        visitions = UserVisit.objects.filter(visit_id=user.pk, visit_type=4)
        # 如果是其他登录用户，就记录访客，本人来访不记录
        if request.user.is_authenticated and request.user.id != pk:
            existed_visition = UserVisit.objects.filter(user=request.user, visit_id=user.pk, visit_type=4)
            if existed_visition:
                existed_visition.update(visit_count=F('visit_count') + 1)
            else:
                visition = UserVisit(user=request.user, visit_id=user.pk, visit_type=4, visit_count=1)
                visition.save()
        # 取出当前用户读过的书
        readed_books = Book.objects.filter(id__in=UserFavorite.objects.filter(fav_type=2, user=user).values('fav_id'))
        return render(request, 'user_center_for_guest.html', {
            'user': user, 'has_follow': has_follow, 'visitions': visitions, 'readed_books': readed_books})

    def post(self, request, pk):
        to_user = UserProfile.objects.get(pk=pk)
        from_user = request.user
        message = request.POST.get('message', '')
        usermsg = UserMessage(from_user_id=from_user.pk, to_user_id=to_user.pk,
                              message=message, has_read=False)
        usermsg.save()
        return redirect('users:user-center-guest', pk=to_user.pk)


class UserInfoView(View):
    def get(self, request):
        return render(request, 'user_center_info.html', {})

    def post(self, request):
        if request.POST.get('submit') == '修改密码':
            update_form = UpdatePwdForm(request.POST)
            if update_form.is_valid():
                pwd1 = update_form.cleaned_data['password1']
                pwd2 = update_form.cleaned_data['password2']
                if pwd1 != pwd2:
                    return render(request, 'user_center_info.html', {'pwdmsg': '两次输入密码不一致！'})
                user = request.user
                user.password = make_password(pwd1)
                user.save()
                # return render(request, 'user_center_info.html', {'pwdmsg': '修改成功！请重新登录！'})
                return redirect('users:login', permanent=True)
            else:
                return render(request, 'user_center_info.html', {'pwdmsg': '密码修改失败！'})
        if request.POST.get('submit') == '修改信息':
            info_form = UpdateUserInfoForm(request.POST, instance=request.user)
            if info_form.is_valid():
                info_form.save()
                return render(request, 'user_center_info.html', {'infomsg': '基本信息修改成功!'})
            else:
                return render(request, 'user_center_info.html', {'infomsg': '基本信息修改失败!'})
        if request.POST.get('submit') == '修改头像':
            image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
            if image_form.is_valid():
                image_form.save()
            return render(request, 'user_center_info.html', {})
        if request.POST.get('submit') == '获取邮箱验证码':
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                return render(request, 'user_center_info.html', {'emailmsg': '邮箱已存在！'})
            send_register_email(email, "update_email")
            return render(request, 'user_center_info.html', {'emailmsg': '验证码已发送！'})
        if request.POST.get('submit') == '修改邮箱':
            email = request.POST.get('email', '')
            request.user.email = email
            request.user.username = email
            request.user.save()
            return redirect("users:login")


class UserNotesView(View):
    def get(self, request):
        # categories = Category.objects.all()
        # tags = Tag.objects.all()
        books = Book.objects.filter(privacy='public').all()
        booknotes_list = BookNotes.objects.filter(user=request.user).order_by('-addtime')
        current_page = request.GET.get('page', 1)
        paginator = Paginator(booknotes_list, per_page=4)
        try:
            booknotes_list = paginator.page(current_page)  # 获取前端传过来显示当前页的数据
        except PageNotAnInteger:
            booknotes_list = paginator.page(1)  # 如果有异常则显示第一页
        except EmptyPage:
            # 如果没有得到具体的分页内容的话,则显示最后一页
            booknotes_list = paginator.page(paginator.num_pages)
        return render(request, 'user_center_notes.html', {'books': books, 'booknotes_list': booknotes_list})

    def post(self, request):
        notes_form = BookNotesForm(request.POST, request.FILES)
        if notes_form.is_valid():
            notes_form.instance.user = request.user
            notes_form.save()
        return redirect('users:user-notes')


class CKeditorDragedAndDropedView(View):
    def post(self, request):
        image = request.FILES['upload']
        if image.name.split('.')[-1] in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
            # 这里的file_path指的是服务器上保存图片的路径
            save_path = settings.MEDIA_ROOT + '/notes/image/' + image.name[-10:]
            file_path = default_storage.save(save_path, image)
            # 获取刚刚保存的文件的url
            file_url = settings.MEDIA_URL + 'notes/image/' + file_path.split('/')[-1]
            # 把文件的url返回给CKEditor
            res = {
                "uploaded": 1,
                "fileName": image.name,
                "url": file_url,
            }
            return HttpResponse(json.dumps(res))
        else:
            message = '扩展名不正确！只接受：' + str(['jpg', 'jpeg', 'png', 'bmp', 'gif'])
            res = {
                "uploaded": 0,
                "error": {
                    "message": message
                }
            }
            return HttpResponse(json.dumps(res))


class UserFavorsViewOld(View):
    def get(self, request):
        # 收藏的文章
        favors = UserFavorite.objects.filter(user=request.user, fav_type=1)
        favor_articles = []
        for fav in favors:
            favor_articles.append(Article.objects.get(id=fav.fav_id))
        # 收藏的图书
        favors = UserFavorite.objects.filter(user=request.user, fav_type=2)
        favor_books = []
        for fav in favors:
            favor_books.append(Book.objects.get(id=fav.fav_id))
        # 收藏的出版机构
        favors = UserFavorite.objects.filter(user=request.user, fav_type=3)
        favor_pubs = []
        for fav in favors:
            favor_pubs.append(Publisher.objects.get(id=fav.fav_id))
        # 收藏的阅读笔记
        favors_ids = UserFavorite.objects.filter(user=request.user, fav_type=4).values_list('fav_id')
        favor_notes = BookNotes.objects.filter(id__in=favors_ids)
        # 收藏的作家
        favors_ids = UserFavorite.objects.filter(user=request.user, fav_type=5).values_list('fav_id')
        favor_authors = Author.objects.filter(id__in=favors_ids)
        return render(request, 'user_center_favors.html', {
            'favor_articles': favor_articles, 'favor_books': favor_books,
            'favor_pubs': favor_pubs, 'favor_notes': favor_notes, 'favor_authors': favor_authors})


class UserFavorsView(View):
    def get(self, request):
        # 收藏的文章
        favors_ids = UserFavorite.objects.filter(user=request.user, fav_type=1).values('fav_id')
        favor_articles = Article.objects.filter(id__in=favors_ids).order_by('-addtime')
        # 收藏的图书
        favors_ids = UserFavorite.objects.filter(user=request.user, fav_type=2).values('fav_id')
        favor_books = Book.objects.filter(id__in=favors_ids).order_by('-addtime')
        # 收藏的出版机构
        favors_ids = UserFavorite.objects.filter(user=request.user, fav_type=3).values('fav_id')
        favor_pubs = Publisher.objects.filter(id__in=favors_ids).order_by('-addtime')
        # 收藏的阅读笔记
        favors_ids = UserFavorite.objects.filter(user=request.user, fav_type=4).values_list('fav_id')
        favor_notes = BookNotes.objects.filter(id__in=favors_ids)
        # 收藏的作家
        favors_ids = UserFavorite.objects.filter(user=request.user, fav_type=5).values_list('fav_id')
        favor_authors = Author.objects.filter(id__in=favors_ids)
        return render(request, 'user_center_favors.html', {
            'favor_articles': favor_articles, 'favor_books': favor_books,
            'favor_pubs': favor_pubs, 'favor_notes': favor_notes, 'favor_authors': favor_authors})


class UserRelationsView(View):
    def get(self, request):
        my_followers_ids = UserFollow.objects.filter(followed=request.user.id).values_list('follower')
        my_followers = UserProfile.objects.filter(id__in=my_followers_ids)
        followed_others_ids = UserFollow.objects.filter(follower=request.user.id).values_list('followed')
        followed_others = UserProfile.objects.filter(id__in=followed_others_ids)
        return render(request, 'user_center_relations.html', {
            'my_followers': my_followers, 'followed_others': followed_others
        })


class UserMessagesView(View):
    def get(self, request):
        usermessages = UserMessage.objects.filter(to_user_id=request.user.pk).order_by('-addtime')
        usermessages.update(has_read=True)  # 批量更新多条记录
        sysnotes = SystemNotefication.objects.filter(user=request.user.pk).order_by('-addtime')
        return render(request, 'user_center_messages.html', {
            'usermessages': usermessages, 'sysnotes': sysnotes})

    def post(self, request):
        msg_id = request.POST.get('msg_id')
        msg_type = request.POST.get('msg_type')
        if msg_type == 'sys-msg':
            sysmsg = SystemNotefication.objects.filter(pk=msg_id).delete()
            return HttpResponse('{"status":"success","msg":"已删除"}', content_type='application/json')
        elif msg_type == 'user-msg':
            usermsg = UserMessage.objects.filter(pk=msg_id).delete()
            return HttpResponse('{"status":"success","msg":"已删除"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"删除失败"}', content_type='application/json')


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response
