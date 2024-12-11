"""
URL configuration for django_travel_agency project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# django_travel_agency/urls.py
from django.contrib import admin
from django.urls import path, include
from home import views  # Make sure you import the homepage view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),  # This maps the root URL to the homepage view
    path('api/bookings/', include('bookings.urls')),  # Include URLs from the bookings app
    path('api/invoices/', include('invoices.urls')),  # Include URLs from the invoices app
    path('api/support/', include('support.urls')),    # Include URLs from the support app
    path('api/news/', include('news.urls')),          # Include URLs from the news app
    path('api/trips/', include('trips.urls')),        # Include URLs from the trips app
    #path('api/accounts/', include('accounts.urls')),  # Include URLs from the accounts app
]


# Add this for media file handling
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)