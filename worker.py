from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_travel_agency.settings')

# Create a Celery application instance
app = Celery('django_travel_agency')

# Load the Celery configuration from the Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# This line is required for Celery 4+ (for compatibility with older versions of Celery).
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
