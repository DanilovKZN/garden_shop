from django.contrib import admin

from users.models import User
from products.admin import BasketAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка пользователя."""
    list_display = ('username', 'image')
    # Inlines добавляет корзину в админку пользователя, так как в product она наследована от admin.TabularInline
    inlines = (BasketAdmin,)
