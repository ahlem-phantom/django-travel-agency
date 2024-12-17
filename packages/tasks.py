from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
from django.core.files.storage import FileSystemStorage
from .models import Booking
import os

# Task to send the confirmation email
@shared_task
def send_confirmation_email(name, email, package_name, total_price):
    subject = f"Booking Confirmation for {package_name}"
    message = render_to_string('booking/confirmation_email.html', {
        'name': name,
        'package_name': package_name,
        'total_price': total_price
    })

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

# Task to generate PDF invoice
@shared_task
def generate_pdf_invoice(booking_id):
    booking = Booking.objects.get(id=booking_id)
    
    # Render invoice HTML template (You need to create the HTML template)
    html_content = render_to_string('booking/invoice.html', {'booking': booking})
    
    # Generate PDF from HTML
    pdf = HTML(string=html_content).write_pdf()

    # Store the PDF file
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'invoices'))
    filename = f'invoice_{booking.id}.pdf'
    fs.save(filename, pdf)

    # Optionally, you could send the invoice as an email attachment or store it in the database
    # send_invoice_email(booking.email, filename)  # Uncomment if you want to send the invoice as an email attachment

    return filename
