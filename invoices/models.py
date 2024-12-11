from django.db import models
from bookings.models import Booking

class Invoice(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    invoice_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice for {self.booking.user} ({self.total_amount})"
