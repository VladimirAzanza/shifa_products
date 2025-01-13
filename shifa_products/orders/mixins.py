from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class OnlyAuthorOrderMixin(UserPassesTestMixin):
    """Mixin to ensure that only the owner of an order can modify it.

    Inherits from:
        - UserPassesTestMixin: Provides the `test_func()` method to check if
        the user has access.

    Methods:
        test_func():
            Checks if the current user is the author (owner) of the order.

        handle_no_permission():
            Redirects to the product list page if the user does not have
            permission to access the order.
    """
    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy('catalog:product_list'))
