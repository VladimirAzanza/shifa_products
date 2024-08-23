from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from .forms import UserForm
from .mixin import GetUserMixin, OnlyAuthorMixin

User = get_user_model()


class ProfileDetailView(OnlyAuthorMixin, GetUserMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address_user'] = self.get_object().addresses.all()
        return context


class ProfileUpdateView(OnlyAuthorMixin, GetUserMixin, UpdateView):
    form_class = UserForm

    def get_success_url(self):
        return reverse_lazy(
            'users:profile',
            kwargs={'username': self.get_object().username}
        )
