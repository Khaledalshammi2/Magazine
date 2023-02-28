from django import template
from django.utils.text import Truncator

register = template.Library()


@register.filter(name='truncatechars')
def truncatechars(value, arg):
    return Truncator(value).chars(arg)
