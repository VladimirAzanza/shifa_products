from django.contrib.auth import get_user_model
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import AddressUserForm, UserUpdateForm
from .mixin import GetUserMixin, OnlyAuthorMixin

User = get_user_model()


class ProfileDetailView(OnlyAuthorMixin, GetUserMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address_user'] = self.get_object().addresses.all()
        return context


class ProfileUpdateView(OnlyAuthorMixin, GetUserMixin, UpdateView):
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            'users:profile',
            kwargs={'username': self.get_object().username}
        )


class AddressUserCreateView(OnlyAuthorMixin, CreateView):
    form_class = AddressUserForm
    template_name = 'users/user_address.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            User,
            pk=self.kwargs.get(self.pk_url_kwarg)
        )

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'users:profile',
            kwargs={'username': self.get_object().username}
        )
