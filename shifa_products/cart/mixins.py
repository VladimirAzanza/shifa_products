from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class OnlyAuthorCartItemMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().cart.user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy('catalog:product_list'))
