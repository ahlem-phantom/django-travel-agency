from django.db import models
from django.contrib.auth.models import User

class SupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_description = models.TextField()
    status = models.CharField(max_length=100, choices=[('open', 'Open'), ('closed', 'Closed')], default='open')

    def __str__(self):
        return f"Ticket {self.id} - {self.status}"
