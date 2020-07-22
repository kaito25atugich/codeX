from django import template
from django.utils import dateformat

register = template.Library()

@register.filter
def add_zero (value):
    return dateformat.format(value,'Y年m月d日')