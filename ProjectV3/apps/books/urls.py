from django.urls import path, include

from books.views import BookListView, BookDetailView, ChapterListView, ArticleDetailView, BookNotesListView, \
    BookNotesDetailView, BookNotesArchiveView, BookNotesDeleteView, BookNotesEditView

app_name = 'books'

urlpatterns = [
    path('book/list/', BookListView.as_view(), name='book-list'),
    path('book/<int:pk>/detail/', BookDetailView.as_view(), name='book-detail'),
    path('<int:pk>/chapter/list/', ChapterListView.as_view(), name='book-read'),
    path('article/<int:pk>/detail/', ArticleDetailView.as_view(), name='article-detail'),
    path('booknotes/list/', BookNotesListView.as_view(), name='booknotes-list'),
    path('booknotes/<int:pk>/detail/', BookNotesDetailView.as_view(), name='booknotes-detail'),
    path('booknotes/delete/', BookNotesDeleteView.as_view(), name='booknotes-delete'),
    path('booknotes/<int:pk>/edit/', BookNotesEditView.as_view(), name='booknotes-edit'),
    path('archive/<int:year>/<int:month>/<int:day>/', BookNotesArchiveView.as_view(),
         name='booknotes_archive'),
]
