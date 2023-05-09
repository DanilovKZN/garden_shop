from django.urls import path

from products.views import products, add_basket, basket_remove


app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:category_id>', products, name='category'),
    path('page/<int:page_number>', products, name='paginator'),
    path('basket/add/<int:product_id>/', add_basket, name='add_basket'),
    path('basket/remove/<int:basket_is>/', basket_remove, name='basket_remove'),
]
