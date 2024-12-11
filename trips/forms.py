from django import forms
from .models import TravelPackage, Rating

class TravelPackageForm(forms.ModelForm):
    class Meta:
        model = TravelPackage
        fields = ['title', 'description', 'tags', 'price', 'image', 'start_date', 'end_date', 'destination']
        widgets = {
            'tags': forms.Select(choices=TravelPackage.TAG_CHOICES),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)])  # Select from 1 to 5
        }
