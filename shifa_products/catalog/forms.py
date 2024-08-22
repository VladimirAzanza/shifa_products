from django import forms
from django.urls import reverse_lazy

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = (
            'title', 'review', 'taste_stars', 'quality_stars', 'location'
        )
