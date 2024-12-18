from django import forms
from .models import TravelPackage, Tag

class TravelPackageForm(forms.ModelForm):
    """
    Form for creating/editing TravelPackage instances.
    Includes fields like name, destination, price, etc.
    """
    class Meta:
        model = TravelPackage
        fields = ['name', 'destination', 'package_type', 'price', 'duration', 'rating', 'description', 'available', 'tags', 'image']

class TagForm(forms.ModelForm):
    """
    Form for creating/editing Tag instances.
    Used for tagging travel packages.
    """
    class Meta:
        model = Tag
        fields = ['name']
