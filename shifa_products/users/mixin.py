from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import CustomUser

User = get_user_model()


class GetUserMixin():
    """Mixin to retrieve a user based on the username from the URL.

    Attributes:
        model (Model): The model to be used.
        pk_url_kwarg (str): The keyword used in the URL for the username.

    Methods:
        get_object():
            Retrieves a user object based on the 'username' parameter in
            the URL.
    """
    model = User
    pk_url_kwarg = 'username'

    def get_object(self):
        username = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(User, username=username)


class OnlyAuthorMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure that only the owner of a user object can modify it.

    Inherits from:
        - LoginRequiredMixin: Requires the user to be logged in.
        - UserPassesTestMixin: Provides the 'test_func()' method to check if
        the user has access.

    Methods:
        test_func():
            Checks if the current user is the owner of the object or
            if the user is staff.

        handle_no_permission():
            Redirects to the homepage if the user does not have permission
            to access the object.
    """
    def test_func(self):
        object = self.get_object()
        if isinstance(object, CustomUser):
            return (
                self.request.user == object or self.request.user.is_staff
            )
        else:
            return (
                self.request.user == object.user or self.request.user.is_staff
            )

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy('pages:index'))
