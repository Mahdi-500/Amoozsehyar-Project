from django import template
from django.db.models import Max, Count
from django.utils.safestring import mark_safe
from ..models import *
from markdown import markdown

register = template.Library()

@register.simple_tag()
def read_time():
    return Post.Publish.annotate(most_time=Max("reading_time")).order_by("-most_time")[:5]

@register.simple_tag()
def most_popular():
    return Post.Publish.annotate(cc=Count("comment")).order_by("-cc")[:5]  # cc = comment_count

@register.simple_tag()
def comment_count(post):
    return post.comment.count()

banned_words = ['Fuck', 'bitch']
@register.filter()
def censore(text):
    for bad in banned_words:
        text = text.replace(bad, "***")
    return mark_safe(markdown(text))