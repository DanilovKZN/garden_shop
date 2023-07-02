from rest_framework import fields, serializers

from products.models import Basket, Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    """Сериализация продуктов на основе модели."""
    # queryset используется, так как в модели продукта категория идет как обязательное поле
    category = serializers.SlugRelatedField(
        queryset=ProductCategory.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'quantity',
            'image',
            'category'
        )


class BasketSerializer(serializers.ModelSerializer):
    """Сериализация корзины."""
    # Чтобы в JSON вместо id товара выдавать словарь с полной информацией о товаре
    product = ProductSerializer()
    # Чтобы добавить сумму однотипных товаров, используя метод из модели Product
    sum = fields.FloatField(required=False)
    # Указывается, чтобы после Meta его описать
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()

    class Meta:
        model = Basket
        fields = (
            'id',
            'product',
            'quantity',
            'total_quantity',
            'sum',
            'created_timestamp',
            'total_sum'
        )
        read_only_fields = ('created_timestamp',)

    def get_total_sum(self, obj):
        """Получаем корзину данного пользователя и заносим итоговую сумму."""
        return Basket.objects.filter(user_id=obj.user.id).total_sum()

    def get_total_quantity(self, obj):
        """Получаем корзину данного пользователя и заносим количество товаров."""
        return Basket.objects.filter(user_id=obj.user.id).total_quantity()
