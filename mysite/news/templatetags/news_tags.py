from django import template
from django.db.models import Count, F
from news.models import Category

register = template.Library()

@register.simple_tag(name='get_categories')
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('news/list_categories.html')
def show_catgories():
    #categories = Category.objects.all()
    #categories = Category.objects.annotate(badge=Count('news')).filter(badge__gte=1)
    categories = Category.objects.annotate(badge=Count('news', filter=F('news__is_published'))).filter(badge__gt=0)
    # мы работаем через связанную модель это надо учитовать, по этому = 'news__is_published'
    return {'categories': categories}