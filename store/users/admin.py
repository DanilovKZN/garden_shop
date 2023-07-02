from django.contrib import admin

from products.admin import BasketAdmin
from users.models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Графа пользователи в админке."""
    list_display = ('username', 'image')
    # Inlines добавляет корзину в админку пользователя, так как в product она наследована от admin.TabularInline
    inlines = (BasketAdmin,)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """Графа подтверждения почты в админке."""
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created', )
