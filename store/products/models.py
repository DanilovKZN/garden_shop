import stripe

from typing import Iterable, Optional

from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    """Категории товаров."""
    name = models.CharField(
        max_length=128,
        verbose_name='Категория',
        help_text='Введите категорию'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
        help_text='Введите описание'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """Товары."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название товара',
        help_text='Введите название товара.'
    )
    description = models.TextField(
        verbose_name='Описание товара',
        help_text='Введите описание товара'
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Цена',
        help_text='Введите стоймость товара'
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество',
        help_text='Введите количество')
    image = models.ImageField(
        upload_to='products_images',
        verbose_name='Изображение'
    )
    stripe_product_price_id = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text='Id товара на stripe.'
    )
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self) -> str:
        return f"Продукт: {self.name} | Категория: {self.category}"

    def save(
        self, force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[Iterable[str]] = None
    ) -> None:
        """Изменяем метод сохранения, чтобы при создании нового объекта в бд
        он создавался и в stripe."""
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
        )

    def create_stripe_product_price(self):
        """Создание цены товара на stripe."""
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),  # так как для stripe цену нужно указывать в копейках (центах)
            currency='rub'
        )
        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    """Переопределяем менеджер для подсчёта итоговой суммы
    и общего количества товаров в корзине."""

    def total_sum(self):
        """Итоговая сумма в корзине."""
        return sum(basket.sum() for basket in self.filter())

    def total_quantity(self):
        """Итоговое количество товара в корзине."""
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        """Для отображения товаров из корзины в момент покупки в stripe."""
        line_items = []

        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }

            line_items.append(item)
        return line_items


class Basket(models.Model):
    """Корзина товаров."""
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    # Используем переопределённый менеджер для корзины
    objects = BasketQuerySet.as_manager()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self) -> str:
        return f"Корзина для {self.user.username} | Продукт: {self.product.name}"

    def sum(self):
        """Цена товаров в корзине"""
        return self.product.price * self.quantity

    def de_json(self):
        """Формируем словарь для передачи в basket history.(Форма order)"""
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        return basket_item

    @classmethod
    def create_or_update(cls, product_id, user):
        """Создание или обновление корзины. Реализован в модели,
        чтобы не дублировать одинаковую логику,
        как для внутрянки, так и для api"""
        basket = Basket.objects.filter(user=user, product_id=product_id)

        if not basket.exists():
            obj = Basket.objects.create(
                user=user,
                product_id=product_id,
                quantity=1
            )
            # Для проверки в api, как флаг создания обьекта в корзине
            is_created = True
            return obj, is_created
        else:
            basket = basket.first()
            basket.quantity += 1
            basket.save()
            is_created = False
            return basket, is_created
