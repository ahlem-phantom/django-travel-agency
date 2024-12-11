from rest_framework import viewsets
from .models import Booking
from .serializers import BookingSerializer
from django.http import HttpResponse

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


def index(request):
    return HttpResponse("This is the invoices index.")
