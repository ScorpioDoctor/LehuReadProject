from django import template

from operations.models import UserFavorite, UserMessage

register = template.Library()


@register.simple_tag
def get_favors_count(user_id):
    return UserFavorite.objects.filter(user_id=user_id).count()


@register.simple_tag
def get_archive_messages(user_id, date):
    return UserMessage.objects.filter(to_user_id=user_id, addtime__year=date.year, addtime__month=date.month,
                                      addtime__day=date.day).order_by('-addtime').all()
