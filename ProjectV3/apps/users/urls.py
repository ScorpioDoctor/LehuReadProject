from django.urls import path, include
from django.views.generic import TemplateView
from .views import LoginView, LogoutView, RegistView, AciveUserView, ForgetPwdView, ResetPwdView, ModifyPwdView, \
    UserCenterView, UserInfoView, UserNotesView, UserFavorsView, UserRelationsView, UserMessagesView, \
    CKeditorDragedAndDropedView, UserCenterGuestView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistView.as_view(), name='register'),
    path('active/<str:active_code>/', AciveUserView.as_view(), name='active-user'),
    path('forgetpwd/', ForgetPwdView.as_view(), name='forgetpwd'),
    path('reset/<str:active_code>/', ResetPwdView.as_view(), name='resetpwd'),
    path('modifypwd/', ModifyPwdView.as_view(), name='modifypwd'),
    # path('updatepwd/', UpdatePwdView.as_view(), name='updatepwd'),
    path('center/', UserCenterView.as_view(), name='user-center'),
    path('center/<int:pk>/guest/', UserCenterGuestView.as_view(), name='user-center-guest'),
    path('center/infos/', UserInfoView.as_view(), name='user-info'),
    path('center/notes/', UserNotesView.as_view(), name='user-notes'),
    path('center/favors/', UserFavorsView.as_view(), name='user-favors'),
    path('center/relations/', UserRelationsView.as_view(), name='user-relations'),
    path('center/messages/', UserMessagesView.as_view(), name='user-messages'),
    path('ckeditor/dragdrop/image/', CKeditorDragedAndDropedView.as_view(), name='ckedt_dragdrop_image'),
]
