from celery import shared_task
from .models import SupportTicket

@shared_task
def process_ticket(ticket_id):
    ticket = SupportTicket.objects.get(id=ticket_id)
    # Process the ticket (this could be integrating with a chatbot or simply updating the status)
    ticket.status = 'closed'
    ticket.save()
