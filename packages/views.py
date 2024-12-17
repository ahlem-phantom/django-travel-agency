from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import TravelPackage, Tag, Booking
from .forms import TravelPackageForm, TagForm
import json
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
import os 
import uuid
from decimal import Decimal
from datetime import date, datetime
from django.contrib import messages
from django.urls import reverse
import requests
from django.core.mail import send_mail
from .tasks import generate_pdf_invoice 

def send_confirmation_email(name, email, package_name, total_price):
    subject = f"Booking Confirmation - {package_name}"
    message = f"""
    Hello {name},

    Thank you for booking your trip with us. Your booking for {package_name} has been successfully confirmed!

    Booking Details:
    - Name: {name}
    - Package: {package_name}
    - Total Price: {total_price} TND

    You will receive an email with all the details shortly.

    If you have any questions, feel free to reach out to us.

    Best regards,
    The Travel Team
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # From email
        [email],  # To email
        fail_silently=False,  # If True, errors will be silently ignored
    )


def load_travel_packages_from_json():
    # Path to your JSON file
    file_path = os.path.join(settings.BASE_DIR, 'travel_packages.json')

    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def book_package(request, pk):
    package = get_object_or_404(TravelPackage, pk=pk)
    return render(request, 'travel_package_booking.html', {'package': package})

def travel_package_list(request):
    travel_packages =  TravelPackage.objects.all()
    ratings_range = range(1, 6)  # Range for star rating
    return render(request, 'travel_package_list.html', {'packages': travel_packages, 'ratings_range': ratings_range}) 
# TravelPackage CRUD views
'''def travel_package_list(request):
    packages = TravelPackage.objects.all()
    return render(request, 'travel_package_list.html', {'packages': packages})
'''
def travel_package_create(request):
    if request.method == 'POST':
        form = TravelPackageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('travel_package_list')
    else:
        form = TravelPackageForm()
    return render(request, 'travel_package_form.html', {'form': form})

def travel_package_update(request, pk):
    package = get_object_or_404(TravelPackage, pk=pk)
    if request.method == 'POST':
        form = TravelPackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            return redirect('travel_package_list')
    else:
        form = TravelPackageForm(instance=package)
    return render(request, 'travel_package_form.html', {'form': form})

def travel_package_delete(request, pk):
    package = get_object_or_404(TravelPackage, pk=pk)
    package.delete()
    return redirect('travel_package_list')

# Tag CRUD views
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'tag_list.html', {'tags': tags})

def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'tag_form.html', {'form': form})

def tag_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm(instance=tag)
    return render(request, 'tag_form.html', {'form': form})

def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    return redirect('tag_list')


def booking_handler_view(request, package_id):
    package = get_object_or_404(TravelPackage, id=package_id)
    child_discount = Decimal('0.5')

    if request.method == 'POST':
        # Fetch form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        booking_date = request.POST.get('datetime')
        num_adults = int(request.POST.get('SelectPerson', 0))
        num_children = int(request.POST.get('SelectKids', 0))
        gender = request.POST.get('SelectGender', 'None')  # Default to 'None'
        payment_method = request.POST.get('payment_method', '0')  # Default to '0' (On Site)
        consent = request.POST.get('consent')

        # Initialize errors list
        errors = {}

        # Server-side validations
        if not name.isalpha() or len(name) < 2:
            errors['name'] = "Name must only contain letters and be at least 2 characters."
        if '@' not in email:
            errors['email'] = "Invalid email address."
        if not booking_date or datetime.strptime(booking_date, '%Y-%m-%d').date() < date.today():
            errors['datetime'] = "The date must be today or a future date."
        if num_adults <= 0:
            errors['SelectPerson'] = "Number of persons must be at least 1."
        if num_children < 0:
            errors['SelectKids'] = "Number of kids cannot be negative."
        if not payment_method:
            errors['payment_method'] = "Payment method is required."
        if not consent:
            errors['consent'] = "You must agree to the terms and conditions."

        # If there are errors, return the same form with errors
        if errors:
            print(f"Error: {errors}")
            return render(request, 'travel_package_booking.html', {
                'package': package,
                'name': name,
                'email': email,
                'booking_date': booking_date,
                'num_adults': num_adults,
                'num_children': num_children,
                'gender': gender,
                'payment_method': payment_method,
                'errors': errors  # Pass errors to the template
            })
        # Calculate total price
        unit_price = package.price
        adults_price = unit_price * num_adults
        children_price = (unit_price * child_discount) * num_children
        total_price = adults_price + children_price

        # Save booking with pending payment
        booking = Booking.objects.create(
            package=package,
            name=name,
            email=email,
            datetime=datetime.strptime(booking_date, '%Y-%m-%d'),
            num_adults=num_adults,
            num_children=num_children,
            total_price=total_price,
            gender=gender,
            payment_status='Pending',  # Default to Pending
            payment_method=payment_method
        )
        
        # If payment method is online, generate payment URL
        if payment_method == "Online":
            payment_url = generate_flouci_payment(total_price)
            if payment_url:
                # Redirect the user to the payment URL
                booking.payment_status = 'Paid'
                booking.save()
                #send_confirmation_email(name, email, package.name, total_price)
                generate_pdf_invoice.delay(booking.id) 
                return HttpResponseRedirect(payment_url)
            else:
                # If the payment URL could not be generated, return an error
                booking.delete()
                return JsonResponse({'error': 'Failed to generate payment URL'}, status=400)
        
        # Return a response or redirect to a confirmation page
        # Redirect to the success page
        send_confirmation_email(name, email, package.name, total_price)
        return redirect(reverse('booking_success'))  # Replace 'success_page' with the actual URL name for the success page

    # If the request is GET, just render the page with the form
    return render(request, 'travel_package_booking.html', {'package': package})


def generate_flouci_payment(amount):
    # Replace with your actual values
    app_token = "8d689544-f77b-43a7-94ab-93ef6b1e7104"
    app_secret = "5727a53a-2033-41a4-839a-294c5e5ea299"
    
    payload = {
        "app_token": app_token,
        "app_secret": app_secret,
        "accept_card": "true",
        "amount": str(int(amount * 100)),  # Amount in smallest unit (e.g., cents)
        "success_link": "http://localhost:8000/packages/success/",
        "fail_link": "http://localhost:8000/packages/fail/",
        "session_timeout_secs": 1200,  # 20 minutes timeout
        "developer_tracking_id": str(uuid.uuid4())  # Optional tracking ID
    }
    
    headers = {
        'Content-Type': 'application/json'
    }

    # Call the Flouci API to generate the payment link
    url = "https://developers.flouci.com/api/generate_payment"
    response = requests.post(url, headers=headers, json=payload)
    
    print(f"Payment Rsponse: {response}")

    if response.status_code == 200:
        payment_data = response.json()
        
        # Handle the successful response
        if payment_data.get("result", {}).get("success"):
            payment_url = payment_data["result"].get("link", '')
            if payment_url:
                return payment_url
            else:
                return None
        else:
            return None
    else:
        return None



def booking_success(request):
    return render(request, 'booking_success.html')  # success.html is the success page template



def booking_fail(request):
    return render(request, 'booking_fail.html')  # success.html is the success page template