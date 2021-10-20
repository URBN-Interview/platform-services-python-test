from django import template

register = template.Library()


@register.filter
def percentage(value):
    if not value:
        return None
    return "{:.0%}".format(value)
