from django import template

register = template.Library()


@register.filter(name="percent")
def percentage(f):
    return "{:.2%}".format(f)
