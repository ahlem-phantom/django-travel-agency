from rest_framework import serializers
from .models import TravelNews

class TravelNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelNews
        fields = ['id', 'title', 'link', 'content', 'published_date', 'image_url', 'category', 'read_time']
