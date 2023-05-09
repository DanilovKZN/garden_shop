from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from products.models import Product, ProductCategory, Basket
from users.models import User


POSTS_IN_PAGE_FOR_PAGINATOR = 3


def paginator(request, post_list):
    """Пагинатор."""
    paginator = Paginator(post_list, POSTS_IN_PAGE_FOR_PAGINATOR)
    page_number = request.GET.get('page', 1)
    page_object = paginator.get_page(page_number)
    return page_object


def index(request):
    """Просто отображение домашней страницы."""
    return render(request, 'products/index.html')


def products(request, category_id=None):
    """Страница продукции, а так же вывод в категориях."""
    category = ProductCategory.objects.all()

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    products_paginator = paginator(request, products)
    context = {
        "title": "Store - каталог",
        "categories": category,
        "products": products_paginator
    }
    return render(request, 'products/products.html', context)


# Декоратор для проверки, что пользователь в системе
@login_required
def add_basket(request, product_id):
    """Добавление товара в корзину."""
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)

    if not basket.exists():
        Basket.objects.create(
            user=request.user,
            product=product,
            quantity=1
        )
    else:
        basket = basket.first()
        basket.quantity += 1
        basket.save()
    # Возврат на страницу, где находится пользователь
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    """Удаление товара из корзины."""
    basket = Basket.objects.get(id=basket_id)
    basket.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
