from rest_framework import serializers
from .models import TravelPackage

class TravelPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPackage
        fields = ['title', 'description', 'price', 'tags', 'image', 'start_date', 'end_date', 'destination', 'created_at']
