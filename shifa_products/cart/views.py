from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView


class AddToCart(LoginRequiredMixin, CreateView):
    pass
