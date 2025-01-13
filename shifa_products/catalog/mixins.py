from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class OnlyAuthorMixin(UserPassesTestMixin):
    """Mixin to ensure that only the author of 'Review' object can modify it.

    Inherits from:
        - UserPassesTestMixin: Provides the 'test_func()' method to check if
        the user has access.

    Methods:
        test_func():
            Checks if the current user is the author of the object.

        handle_no_permission():
            Redirects to the product detail page if the user does not have
            permission to access the object.
    """
    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(
            reverse_lazy(
                'catalog:product_detail',
                kwargs={'product_id': self.get_object().product.id}
            )
        )
