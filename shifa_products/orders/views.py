from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View
from weasyprint import HTML

from .forms import OrderForm
from .mixins import OnlyAuthorOrderMixin
from .models import Order, OrderItem
from cart.models import Cart
from shifa_products.constants import TELEGRAM_MESSAGE
from shifa_products.telegram_notifications import send_notification


class OrderCreateView(CreateView):
    """View for creating a new order and processing the cart items.

    Inherits from:
        - CreateView: Handles the creation of a new 'Order' object.

    Attributes:
        model (Model): The model associated with the view 'Order'.
        form_class (Form): The form class used to create 'Order'.

    Methods:
        form_valid(form):
            Adds the user to the order, processes the cart items, deletes
            the cart, and sends a Telegram notification.

        get_success_url():
            Returns the URL to redirect to after successfully creating
            the order.
    """
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        order = form.save()
        cart = get_object_or_404(
            Cart, user=user
        )
        cart_items = cart.cart_items.all()
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
        cart.delete()
        send_notification(
            message=TELEGRAM_MESSAGE.format(
                first_name=user.first_name,
                last_name=user.last_name
            )
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'orders:order_detail',
            kwargs={'order_id': self.object.pk}
        )


class OrderDetailView(OnlyAuthorOrderMixin, DetailView):
    """View for displaying the details of a specific order.

    Inherits from:
        - OnlyAuthorOrderMixin: Restricts access to the order owner.
        - DetailView: Displays a single 'Order' object.

    Attributes:
        model (Model): The model associated with the view 'Order'.
        pk_url_kwarg (str): The URL keyword used to identify the order.

    Methods:
        get_context_data(**kwargs):
            Adds order items and calculates the total for the order to
            the context.
    """
    model = Order
    pk_url_kwarg = 'order_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.get_object().order_items.annotate(
            total_item=F('quantity') * F('product__price')
        )
        context['order_total'] = self.get_object().order_items.aggregate(
            order_total=Sum(F('quantity') * F('product__price'), default=0)
        )['order_total']
        return context


class OrderListView(LoginRequiredMixin, ListView):
    """View for listing all orders for the currently logged-in user.

    Inherits from:
        - LoginRequiredMixin: Ensures the user is authenticated.
        - ListView: Displays a list of 'Order' objects.

    Attributes:
        paginate_by (int): Number of orders per page.

    Methods:
        get_queryset():
            Filters orders to display only the ones associated with the
            current user.
    """
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderPdfPrintView(OnlyAuthorOrderMixin, View):
    """View for generating and downloading a PDF of a specific order.

    Inherits from:
        - OnlyAuthorOrderMixin: Restricts access to the order owner.
        - View: Provides basic functionality for handling HTTP requests.

    Methods:
        get_object():
            Retrieves the 'Order' object associated with the URL parameter
            `order_id`.

        get(request, *args, **kwargs):
            Generates the PDF for the order and returns it as an HTTP response.
    """
    def get_object(self):
        return get_object_or_404(
            Order,
            pk=self.kwargs.get('order_id'),
            user=self.request.user
        )

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        order_items = order.order_items.annotate(
            total_item=F('quantity') * F('product__price')
        )
        order_total = order.order_items.aggregate(
            order_total=Sum(F('quantity') * F('product__price'), default=0)
        )['order_total']
        context = {
            'order': order,
            'order_items': order_items,
            'order_total': order_total
        }
        html_template = render_to_string('orders/order_to_pdf.html', context)
        pdf_file = HTML(string=html_template).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = (
            f'attachment; filename="order_{order.id}.pdf"'
        )
        return response
