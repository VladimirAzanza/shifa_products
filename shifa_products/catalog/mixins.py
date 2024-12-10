from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(
            reverse_lazy(
                'catalog:product_detail',
                kwargs={'product_id': self.get_object().product.id}
            )
        )
