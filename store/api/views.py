from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import Basket, Product
from products.serializers import BasketSerializer, ProductSerializer

PRODUCT_NOT_IN_BASKET = "Товара с таким ID не существует!"
FIELD_IS_REQUIRED = "Это поле обязательно к заполнению!"


class ProductModelViewSet(ModelViewSet):
    """Работа с продуктами."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        """Переопределение, для выдачи прав на создание,
        редактирование и удаление только Админу."""
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        return super(ProductModelViewSet, self).get_permissions()


class BasketModelViewSet(ModelViewSet):
    """Работа с корзиной."""
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Переопределяем метод, чтобы выводить корзину
        только конкретного пользователя."""
        queryset = super(BasketModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            """Переопределяем метод."""
            # Достаем данные (id товара) из тела запроса
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)
            # Если несуществует такого продукта
            if not products.exists():
                return Response(
                    {'product_id': PRODUCT_NOT_IN_BASKET},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Создаем товар в корзине с помощью нашего переопределённого в models метода и получем флаг
            obj, is_created = Basket.create_or_update(products.first().id, self.request.user)
            # Если товар добавлен в корзину впервые, то статус 201, если обновлён то 200
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            # get_serializer() берёт BasketSerializer
            serializer = self.get_serializer(obj)
            # Возвращаем наш созданный товар из тела запроса
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response(
                {'product_id': FIELD_IS_REQUIRED},
                status=status.HTTP_400_BAD_REQUEST
            )
