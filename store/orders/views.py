from http import HTTPStatus
from typing import Any, Dict

import stripe
from django.conf import settings
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.mixins import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket


TITLE_ORDER = 'Store - оформление заказа'
TITLE_SUCCESS_TEMPLATE = 'Store - Спасибо за заказ!'
TITLE_ORDERS = 'Store - заказы'

# Глобальная переменная для работы со Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    """Формирование шаблона удачной покупки."""
    template_name = 'orders/success.html'
    title = TITLE_SUCCESS_TEMPLATE


class CanceledTemplateView(TemplateView):
    """Формирование шаблона неудачного исхода."""
    # Пока как заглушка при неудачном исходе
    template_name = 'orders/canceled.html'


class OrdersListView(TitleMixin, ListView):
    """Формирование шаблона заказов с выводом всех заказов пользователя."""
    template_name = 'orders/orders.html'
    title = TITLE_ORDERS
    queryset = Order.objects.all()
    ordering = ('-created',)

    def get_queryset(self):
        """Переопределяем вывод всех заказов из БД для вывода только заказов пользователя."""
        super(OrdersListView, self).get_queryset()
        return Order.objects.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    """Формирование шаблона и информации о заказе пользователя."""
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Переопределяем, для вывода в титуле номера заказа."""
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - заказ №{self.object.id}'
        return context


class OrderCreateView(TitleMixin, CreateView):
    """Создание заказа."""
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = TITLE_ORDER

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Создание чекаут сессии для работы с платёжной системой Stripe."""
        super(OrderCreateView, self).post(request, *args, **kwargs)
        # Берём корзину пользователя совершающего покупку
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        # Берём объект формы (instance) и в нём уже initiator
        # и закидываем туда пользователя из запроса
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


# WebHook stripe
@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        fulfill_order(session)

    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
