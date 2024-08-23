from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView


User = get_user_model()


class ProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    pk_url_kwarg = 'username'

    def get_object(self):
        username = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(User, username=username)

    def test_func(self):
        object = self.get_object()
        return self.request.user == object or self.request.user.is_staff

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy('pages:index'))
