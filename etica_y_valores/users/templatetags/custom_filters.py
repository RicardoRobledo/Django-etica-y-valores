import os
from django import template


register = template.Library()


@register.filter
def basename(value):
    """Return the basename of a file path."""
    return os.path.basename(value)
