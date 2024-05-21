from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from goods.models import Products
from carts.models import Cart
from carts.utils import get_user_carts


def cart_add(request):

    product_id = request.POST.get("product_id")

    product = get_object_or_404(Products, id=product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    else:
        carts = Cart.objects.filter(
            session_key=request.session.session_key, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(
                session_key=request.session.session_key, product=product, quantity=1)

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request
    )

    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)


def cart_change(request):

    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()

    user_cart = get_user_carts(request)

    current_path = '/'+'/'.join(request.META['HTTP_REFERER'].split('/')[3:])
    order_url = reverse("orders:create_order")

    if current_path == order_url:
        order = True
    else:
        order = False

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart, "order": order}, request=request
    )

    if len(user_cart) == 0 and current_path == order_url:
        redirect_to_home = True
    else:
        redirect_to_home = False

    response_data = {
        "message": "Количество изменено",
        "cart_items_html": cart_items_html,
        "redirect_to_home": redirect_to_home
    }

    return JsonResponse(response_data)


def cart_remove(request):

    cart_id = request.POST.get("cart_id")

    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_cart = get_user_carts(request)

    current_path = '/'+'/'.join(request.META['HTTP_REFERER'].split('/')[3:])
    order_url = reverse("orders:create_order")

    if current_path == order_url:
        order = True
    else:
        order = False

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart, "order": order}, request=request
    )

    if len(user_cart) == 0 and current_path == order_url:
        redirect_to_home = True
    else:
        redirect_to_home = False

    response_data = {
        "message": "Товар удален",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
        "redirect_to_home": redirect_to_home
    }

    return JsonResponse(response_data)
