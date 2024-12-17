from celery import shared_task
from weasyprint import HTML

@shared_task
def generate_invoice_pdf(booking_id):
    # Retrieve booking data from the database
    booking = Booking.objects.get(id=booking_id)
    
    # Prepare the invoice data
    invoice_html = render_to_string('invoice_pdf.html', {'booking': booking})
    
    # Generate PDF from HTML
    pdf = HTML(string=invoice_html).write_pdf()
    
    # Save the generated PDF (store it in the media directory)
    invoice_file_path = f'media/invoices/invoice_{booking.id}.pdf'
    with open(invoice_file_path, 'wb') as f:
        f.write(pdf)
    
    return invoice_file_path






'''
from celery import shared_task
#from weasyprint import HTML
from io import BytesIO
from django.core.files import File
from .models import Invoice

@shared_task
def generate_invoice_pdf(invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    .git\html = HTML(string=f"Invoice for {invoice.booking.user} - Total: {invoice.total_amount}")
    pdf_file = html.write_pdf()
    
    # Save the generated PDF as a file
    file_name = f"invoice_{invoice.id}.pdf"
    file = BytesIO(pdf_file)
    django_file = File(file, name=file_name)
    # Save it to the invoice model
    invoice.pdf.save(file_name, django_file, save=True)

    '''
