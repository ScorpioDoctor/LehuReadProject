from django.urls import path, include
from django.views.generic import TemplateView

from organizations.views import PublisherListView, PublisherDetailView, AuthorDetailView

app_name = 'organizations'

urlpatterns = [
    path('publishers/', PublisherListView.as_view(), name='publisher-list'),
    path('publisher/<int:pk>/detail/', PublisherDetailView.as_view(), name='publisher-detail'),
    path('author/<int:pk>/detail/', AuthorDetailView.as_view(), name='author-detail'),
]
