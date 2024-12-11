from celery import shared_task
from django.core.mail import send_mail
from .models import Booking

@shared_task
def send_booking_confirmation_email(booking_id):
    booking = Booking.objects.get(id=booking_id)
    send_mail(
        'Booking Confirmation',
        f"Your booking to {booking.destination} is confirmed!",
        'from@example.com',
        [booking.user.email],
        fail_silently=False,
    )
