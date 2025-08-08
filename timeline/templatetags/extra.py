from django import template

register = template.Library()

@register.filter
def is_list(value):
    return isinstance(value, (list, tuple))

@register.filter
def as_csv(value):
    if isinstance(value, (list, tuple)):
        return ", ".join(str(v) for v in value)
    return value
