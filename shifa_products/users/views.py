from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import AddressUserForm, UserUpdateForm
from .mixin import GetUserMixin, OnlyAuthorMixin
from .models import AddressUser
from shifa_products.constants import ADDRESS_AT_ORDERS_MESSAGE


User = get_user_model()


class ProfileDetailView(OnlyAuthorMixin, GetUserMixin, DetailView):
    """View for displaying the profile details of a user, including addresses.

    Inherits from:
        - OnlyAuthorMixin: Restricts access to the profile of the user.
        - GetUserMixin: Retrieves the user object based on the URL parameter.
        - DetailView: Displays the details of a single 'User' object.

    Methods:
        get_context_data(**kwargs):
            Adds the user's addresses to the context for rendering the profile
            view.
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address_user'] = self.get_object().addresses.all()
        return context


class ProfileUpdateView(OnlyAuthorMixin, GetUserMixin, UpdateView):
    """View for updating the user's profile information.

    Inherits from:
        - OnlyAuthorMixin: Restricts access to the profile of the user.
        - GetUserMixin: Retrieves the user object based on the URL parameter.
        - UpdateView: Displays and handles the update form for 'User' object.

    Attributes:
        form_class (Form): The form used to update the user's profile.

    Methods:
        get_success_url():
            Returns the URL to redirect to after successfully updating
            the profile.
    """
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            'users:profile',
            kwargs={'username': self.get_object().username}
        )


class AddressUserCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new address for the logged-in user.

    Inherits from:
        - LoginRequiredMixin: Ensures the user is authenticated.
        - CreateView: Handles the creation of a new 'AddressUser' object.

    Attributes:
        model (Model): The model associated with the view 'AddressUser'.
        form_class (Form): The form used to create a new address.
        template_name (str): The template used to render the address.

    Methods:
        form_valid(form):
            Assigns the current user to the address and saves the address.

        get_success_url():
            Returns the URL to redirect to after successfully creating the
            address.
    """
    model = AddressUser
    form_class = AddressUserForm
    template_name = 'users/user_address.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'users:profile',
            kwargs={'username': self.request.user.username}
        )


class AddressUserDeleteView(OnlyAuthorMixin, DeleteView):
    """View for deleting an address associated with the logged-in user.

    Inherits from:
        - OnlyAuthorMixin: Restricts access to the owner of the address.
        - DeleteView: Handles the deletion of an 'AddressUser' object.

    Attributes:
        model (Model): The model associated with the view 'AddressUser'.
        pk_url_kwarg (str): The URL keyword used to identify the address.

    Methods:
        get(request, *args, **kwargs):
            Handles the address deletion, preventing deletion if the
            address is associated with any orders.

        get_success_url():
            Returns the URL to redirect to after successfully deleting
            the address.
    """
    model = AddressUser
    pk_url_kwarg = 'address_id'

    def get(self, request, *args, **kwargs):
        address = self.get_object()
        if address.orders.exists():
            messages.error(request, ADDRESS_AT_ORDERS_MESSAGE)
            return redirect('users:profile', username=address.user.username)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'users:profile',
            kwargs={'username': self.request.user.username}
        )
