from django.shortcuts import get_object_or_404, render
from goods.models import Categories, Products


def catalog(request, category_slug=False):

    bmvd = False
    category = False
    parent_categories = False
    categories = False
    goods = Products.objects.none()

    if category_slug:

        category = get_object_or_404(Categories, slug=category_slug)

        if category_slug == "pticevodstvo":
            parent_categories = category.get_ancestors(include_self=True)
            categories = category.get_children()
            goods = Products.objects.filter(category__in=categories)

        elif category_slug in get_object_or_404(
            Categories, slug="pticevodstvo"
        ).get_children().values_list("slug", flat=True):
            parent_categories = category.get_ancestors(include_self=True)
            categories = get_object_or_404(
                Categories, slug="pticevodstvo"
            ).get_children()
            goods = Products.objects.filter(category__slug=category_slug)

        elif category_slug == "bmvd":
            bmvd = True
            goods = Products.objects.filter(category__slug=category_slug)

        else:
            parent_categories = category.get_ancestors(include_self=True)
            bmvd_category = get_object_or_404(Categories, slug='bmvd')
            categories = Categories.objects.exclude(id=bmvd_category.id)
            goods = Products.objects.filter(category__slug=category_slug)

        title = f"Каталог {category.name} | БиоКормЭксперт"

    else:
        bmvd_category = get_object_or_404(Categories, slug='bmvd')
        categories = Categories.objects.exclude(id=bmvd_category.id)
        goods = Products.objects.exclude(category=bmvd_category)
        title = "Каталог Комбикорма | БиоКормЭксперт"

    context = {
        "title": title,
        "bmvd": bmvd,
        "category": category,
        "parent_categories": parent_categories,
        "categories": categories,
        "goods": goods,
    }

    return render(request, "goods/catalog.html", context)


def product(request, product_slug):

    product = Products.objects.get(slug=product_slug)

    if product.category.slug == "bmvd":
        bmvd_product = True
        parent_categories = False
    else:
        bmvd_product = False
        parent_categories = product.category.get_ancestors(include_self=True)

    if bmvd_product:
        title = f"БМВД {product.name} | БиоКормЭксперт"
    else:
        title = f"Комбикорм {product.name} | БиоКормЭксперт"

    if product.advantages:
        advantages_list = product.advantages.split("\n")
    else:
        advantages_list = None

    if product.nutritional_info:
        nutritional_info_lines = product.nutritional_info.split("\n")
        nutritional_info_list = []
        for nutritional_info in nutritional_info_lines:
            nutritional_info_list.append(nutritional_info.split(";"))
    else:
        nutritional_info_list = None

    if product.composition:
        composition_list = product.composition.split("\n")
    else:
        composition_list = None

    if bmvd_product:
        if product.feeding_standards:
            feeding_standards_lines = product.feeding_standards.split("\n")
            feeding_standards_list = []
            for feeding_standard in feeding_standards_lines:
                feeding_standards_list.append(feeding_standard.split(";"))
        else:
            feeding_standards_list = None
    else:
        if product.feeding_standards:
            feeding_standards_list = product.feeding_standards.split("\n")
        else:
            feeding_standards_list = None

    if product.recommendations:
        recommendations_list = product.recommendations.split("\n")
    else:
        recommendations_list = None

    context = {
        "title": title,
        "product": product,
        "bmvd_product": bmvd_product,
        "advantages_list": advantages_list,
        "nutritional_info_list": nutritional_info_list,
        "composition_list": composition_list,
        "feeding_standards_list": feeding_standards_list,
        "recommendations_list": recommendations_list,
        "parent_categories": parent_categories,
    }

    return render(request, "goods/product.html", context)
