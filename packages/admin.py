from django.contrib import admin
from .models import TravelPackage, Tag, Booking

@admin.register(TravelPackage)
class TravelPackageAdmin(admin.ModelAdmin):
    """
    Admin interface for managing TravelPackage models.
    Provides functionalities to display essential fields and search by package name,
    destination, and associated tag names.
    """
    list_display = ('name', 'destination', 'price', 'rating', 'available', 'duration')
    search_fields = ('name', 'destination', 'tags__name')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Tag models.
    Allows the viewing and searching of tags by name.
    """
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Booking models.
    Allows the viewing, searching, and filtering of booking data, including package,
    payment status, and payment method.
    """
    list_display = ('name', 'email', 'num_adults', 'num_children', 'payment_method', 'payment_status', 'total_price', 'datetime', 'package')
    search_fields = ('name', 'email', 'package__name')
    list_filter = ('payment_status', 'payment_method', 'package')