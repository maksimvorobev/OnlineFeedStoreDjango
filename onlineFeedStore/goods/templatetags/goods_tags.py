from django import template
from django.shortcuts import get_object_or_404

from goods.models import Categories, Products


register = template.Library()


@register.simple_tag()
def tag_categories_kombi():
    bmvd_category = get_object_or_404(Categories, slug='bmvd')
    return Categories.objects.exclude(id=bmvd_category.id)

@register.simple_tag()
def tag_product_bmvd():
    bmvd_category = get_object_or_404(Categories, slug='bmvd')
    return Products.objects.filter(category=bmvd_category)
