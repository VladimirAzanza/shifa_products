from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import AddressUser, CustomUser


class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')


class AddressUserForm(forms.ModelForm):
    class Meta:
        model = AddressUser
        fields = ('location', 'street', 'postal_code')
