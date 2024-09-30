from django import forms

from .models import Review
from .validators import validate_stars


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = (
            'title', 'review', 'taste_stars', 'quality_stars', 'location'
        )

    def clean_taste_stars(self):
        taste_stars = self.cleaned_data.get('taste_stars')
        return validate_stars(taste_stars)

    def clean_quality_stars(self):
        quality_stars = self.cleaned_data.get('quality_stars')
        return validate_stars(quality_stars)
