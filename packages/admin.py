from django.contrib import admin
from .models import TravelPackage, Tag, Booking

@admin.register(TravelPackage)
class TravelPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'price', 'rating', 'available', 'duration')
    search_fields = ('name', 'destination', 'tags__name')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'num_adults', 'num_children', 'payment_method', 'payment_status', 'total_price', 'datetime', 'package')
    search_fields = ('name', 'email', 'package__name')
    list_filter = ('payment_status', 'payment_method', 'package')