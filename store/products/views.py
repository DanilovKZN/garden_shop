from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.mixins import TitleMixin
from products.models import Basket, Product, ProductCategory


POSTS_IN_PAGE_FOR_PAGINATOR = 6


class IndexView(TitleMixin, TemplateView):
    """Классовое представление главной страницы."""
    template_name = 'products/index.html'
    title = '6 соток'


class ProductsListView(TitleMixin, ListView):
    """Вывод продукции магазина. Если пришёл category_id,
    то выводим только товары выбранной категории."""
    model = Product
    title = '6 соток - каталог'
    template_name = 'products/products.html'
    paginate_by = POSTS_IN_PAGE_FOR_PAGINATOR

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        # достаем из kwargs наш id категории
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


# Декоратор для проверки, что пользователь в системе
@login_required
def add_basket(request, product_id):
    """Добавление товара в корзину."""
    Basket.create_or_update(product_id, request.user)
    # Возврат на страницу, где находится пользователь
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    """Удаление товара из корзины."""
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
