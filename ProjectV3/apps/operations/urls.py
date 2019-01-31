from django.urls import path, include
from .views import AddFavView, UserAskView, UserCommentView, UserFollowView

app_name = 'operations'

urlpatterns = [
    path('favor/', AddFavView.as_view(), name='add-fav'),
    path('ask/', UserAskView.as_view(), name='user-ask'),
    path('comment/', UserCommentView.as_view(), name='user-comment'),
    path('follow/', UserFollowView.as_view(), name='user-follow'),

]
