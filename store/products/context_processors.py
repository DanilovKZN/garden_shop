from products.models import Basket


def baskets(request):
    """Контекстный процессор для вывода корзины пользователя.
    Если пользователь не авторизован, то выдаёт пустой список."""
    user = request.user
    return_list = []
    if user.is_authenticated:
        return_list = Basket.objects.filter(user=user)
    return {"baskets": return_list}
