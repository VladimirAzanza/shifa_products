from django import forms

from .models import Cart, CartItem


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ('quantity',)


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'
