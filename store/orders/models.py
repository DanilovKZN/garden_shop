from django.db import models

from products.models import Basket
from users.models import User


class Order(models.Model):
    """Модель заказа."""
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3

    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Заказ №{self.id} для {self.first_name} {self.last_name}'

    def update_after_payment(self) -> None:
        """Обновление заказа после оплаты."""
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        # Формирование списка купленных товаров. Каждый товар имеет название, цену, количество...
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum())
        }
        baskets.delete()
        self.save()
