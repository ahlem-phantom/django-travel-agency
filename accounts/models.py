from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any custom fields here (e.g., preferences, profile_picture, etc.)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Avoid conflict with default User
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Avoid conflict with default User
        blank=True,
    )

    def __str__(self):
        return self.username
