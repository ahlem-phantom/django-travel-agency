from django import forms
from .models import TravelPackage

class TravelPackageForm(forms.ModelForm):
    class Meta:
        model = TravelPackage
        fields = ['title', 'description', 'tags', 'price', 'image', 'start_date', 'end_date', 'destination']
        widgets = {
            'tags': forms.Select(choices=TravelPackage.TAG_CHOICES),
        }
