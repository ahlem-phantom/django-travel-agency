from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
from django.core.files.storage import FileSystemStorage
from .models import Booking
import os
from django.core.files.base import ContentFile
import datetime
# Task to send the confirmation email
@shared_task
def send_confirmation_email(name, email, package_name, total_price):
    subject = f"Booking Confirmation for {package_name}"
    print('Sending email...')
    message = render_to_string('confirmation_email.html', {
        'name': name,
        'package_name': package_name,
        'total_price': total_price
    })
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=message  # This ensures the email is sent as HTML
    )

# Task to generate PDF invoice
@shared_task
def generate_pdf_invoice(booking_id):
    booking = Booking.objects.get(id=booking_id)
    discount = (booking.package.price * 50 / 100) * booking.num_children
    today = datetime.date.today()
    print('Generating PDF invoice...')

    # Render invoice HTML template
    html_content = render_to_string('invoice.html', {'booking': booking, 'discount': discount, 'today': today})

    # Generate PDF from HTML
    pdf = HTML(string=html_content).write_pdf()

    # Store the PDF file using FileSystemStorage
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'invoices'))
    filename = f'invoice_{booking.id}.pdf'
    pdf_file = ContentFile(pdf)  # Wrap bytes into a file-like object

    fs.save(filename, pdf_file)

    print(f'PDF invoice saved as {filename}')

    return filename



