from django import template
from ..models import *
from django.db.models import Max

register = template.Library()

@register.simple_tag()
def read_time():
    return Post.Publish.annotate(most_time=Max("reading_time")).order_by("-most_time")[:5]