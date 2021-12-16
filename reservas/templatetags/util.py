from django import template
from django.db.models.query import QuerySet
import datetime
register = template.Library()


@register.filter(name='type_date')
def type_date(value):
    if isinstance(value, datetime.date) or isinstance(value, datetime.time):
        return True
    else:
        return False


@register.filter(name='type_query')
def type_query(value):
    if isinstance(value, QuerySet):
        return True
    else:
        return False
