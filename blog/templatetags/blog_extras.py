from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.template.defaultfilters import linebreaksbr, urlize
import datetime
from django.template.defaultfilters import stringfilter


register = template.Library()
@stringfilter
@register.filter(name="custom_stringify")
def custom_stringify(value):
    return str(value)