# home/views.py
from django.http import HttpResponse

def homepage(request):
    return HttpResponse("Welcome to the Travel Agency!")
