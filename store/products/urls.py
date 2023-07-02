from django.urls import path

from products.views import ProductsListView, add_basket, basket_remove


app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>', ProductsListView.as_view(), name='category'),
    path('page/<int:page>', ProductsListView.as_view(), name='paginator'),
    path('basket/add/<int:product_id>/', add_basket, name='add_basket'),
    path('basket/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
