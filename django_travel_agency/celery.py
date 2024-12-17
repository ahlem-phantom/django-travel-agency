from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_travel_agency.settings')

app = Celery('django_travel_agency', broker='pyamqp://guest@localhost//')


app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.result_backend = 'db+sqlite:///db.sqlite3'
app.conf.worker_pool = 'solo'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()



