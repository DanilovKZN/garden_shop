from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):
    """Тестирование главной страницы.
    Каждый метод должен начинаться со слова test."""

    def test_view(self):
        # Получаем ссылку
        path = reverse('index')
        # Делаем запрос
        response = self.client.get(path)

        # Ответ 200?
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Есть ли контекст-дата, а в ней Store?
        self.assertEqual(response.context_data['title'], 'Store')

        # Тот ли шаблон?
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    """Тестирование вывода продукции магазина. """

    fixtures = ['categories.json', 'goods.json']

    # Хранилище переменных, используемых в разных тестах для соблюдения DRY
    def setUp(self) -> None:
        self.products = Product.objects.all()

    def _common_tests(self, response):
        """Вынос одинаковых тестов в классе."""
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - каталог')
        self.assertTemplateUsed(response, 'products/products.html')

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        # Те ли 3 продукта подгрузились на главную страницу?
        # list() иначе qveryset не будут равны
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_tests(response)

        # При выборе категории точно ли подгрузились продукты данной категории?
        print(list(response.context_data['object_list']))
        print(list(self.products.filter(category_id=category.id)))
        self.assertEqual(
            list(response.context_data['object_list']),
            list(response.context_data['paginator'].page(1).object_list)
        )
