from django.db import models

from users.models import User


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
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self) -> str:
        return f"Продукт: {self.name} | Категория: {self.category}"


class BasketQuerySet(models.QuerySet):
    """Переопределяем менеджер для подсчёта итоговой суммы
    и общего количества товаров в корзине."""

    def total_sum(self):
        return sum(basket.sum() for basket in self.filter())
    
    def total_quatity(self):
        return sum(basket.quantity for basket in self)


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
    