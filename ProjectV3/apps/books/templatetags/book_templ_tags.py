from django import template
from django.db.models import QuerySet

from books.models import Category, Tag, Book, Epoch, LanguageKind, BookNotes
from operations.models import ArticleComment, BookNotesComment

register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.simple_tag
def get_tags():
    return Tag.objects.all()


@register.simple_tag
def get_epochs():
    return Epoch.objects.all()


@register.simple_tag
def get_languages():
    return LanguageKind.objects.all()


@register.filter
def get_styles(value):
    styles = ['primary', 'success', 'warning', 'danger', 'info', 'dark', 'light']
    return styles[value % len(styles)]


@register.simple_tag
def get_all_books():
    return Book.objects.filter(privacy='public').all()


@register.simple_tag
def get_hotest_books(num=5):
    return Book.objects.filter(privacy='public').all().order_by('-clicknum')[:num]


@register.simple_tag
def get_tag_related_books(pk, maxcount=6):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        book = Book.objects.first()
    booktags = book.tags.all()
    related_books = set()
    for tag in booktags:
        # related_books.add(Book.objects.filter(tags=tag, privacy='public'))#不能用add的原因
        related_books.update(Book.objects.filter(tags=tag, privacy='public').distinct())
    return list(related_books)[:maxcount]


@register.simple_tag
def get_category_related_books(pk, maxcount=6):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        book = Book.objects.first()
    return Book.objects.filter(category=book.category, privacy='public').exclude(pk=book.pk)[:maxcount]


@register.simple_tag
def get_category_related_booknotes(ctg_id, notes_pk, maxcount=6):
    return BookNotes.objects.filter(privacy='public', category_id=ctg_id).exclude(pk=notes_pk)[:maxcount]


@register.filter(name='range')
def my_range(number):
    return range(0, number)


@register.simple_tag
def get_article_comments(article_pk):
    return ArticleComment.objects.filter(article_id=article_pk).order_by('-addtime')


@register.simple_tag
def get_hotest_booknotes(num=5):
    return BookNotes.objects.filter(privacy='public').all().order_by('-clicknum')[:num]


@register.simple_tag
def get_archive_dates():
    return BookNotes.objects.dates('addtime', 'day', order='DESC')


@register.simple_tag
def get_booknotes_comments(pk):
    return BookNotesComment.objects.filter(booknotes_id=pk).order_by('-addtime')
