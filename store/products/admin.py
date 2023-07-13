from django.contrib import admin

from products.models import Basket, Product, ProductCategory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка продукции."""
    list_display = ('name', 'price', 'quantity', 'category')
    # Кортеж в кортеже для расположения на одной строке
    fields = ('image', 'name', 'description', ('price', 'quantity'), 'stripe_product_price_id', 'category')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    """Админка категории продукции."""
    list_display = ('name',)
    fields = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


# TabularInline используется, так как у нас есть ForeignKey связь
class BasketAdmin(admin.TabularInline):
    """Отображается в адмике User."""
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    # Так как дату изменять вручную нельзя
    readonly_fields = ('created_timestamp',)
    # Убираем дополнительные строки, по умолчанию идут 3 пустых строки
    extra = 0
