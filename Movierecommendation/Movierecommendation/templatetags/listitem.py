from django import template

register = template.Library()

@register.filter
def listitem(sequence, position):
    return sequence[position]