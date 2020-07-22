from django import template

register = template.Library()

@register.filter
def get_array_value(arr, value):
    return arr[value]