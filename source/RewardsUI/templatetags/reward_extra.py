import math
from django import template

register = template.Library()

@register.filter(name="mutiple")
def mutiple(n1, n2):
    return math.floor(n1 * n2)