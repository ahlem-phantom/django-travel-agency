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
from .tasks import generate_pdf_invoice, send_confirmation_email , top_recommendations
from django.db.models import Q
import numpy as np  # NumPy for calculations
from celery.result import AsyncResult
from django.conf import settings



def book_package(request, pk):
    package = get_object_or_404(TravelPackage, pk=pk)
    return render(request, 'travel_package_booking.html', {'package': package})

def travel_package_list(request):
    travel_packages =  TravelPackage.objects.all()
    ratings_range = range(1, 6)  # Range for star rating
    return render(request, 'travel_package_list.html', {'packages': travel_packages, 'ratings_range': ratings_range}) 

def validate_booking(name, email, booking_date, num_adults, num_children, payment_method, consent):
    errors = {}
    if len(name) < 2:
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
    return errors


def calculate_total_price(package, num_adults, num_children, child_discount):
    unit_price = package.price
    adults_price = unit_price * num_adults
    children_price = (unit_price * child_discount) * num_children
    return adults_price + children_price


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



# Booking handler view
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
        errors = validate_booking(name, email, booking_date, num_adults, num_children, payment_method, consent)

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
        total_price = calculate_total_price(package, num_adults, num_children, child_discount)

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
                send_confirmation_email.apply_async(args=[name, email, package.name, total_price])
                generate_pdf_invoice.delay(booking.id) 
                return HttpResponseRedirect(payment_url)
            else:
                # If the payment URL could not be generated, return an error
                booking.delete()
                return JsonResponse({'error': 'Failed to generate payment URL'}, status=400)
        
        # Return a response or redirect to a confirmation page
        # Redirect to the success page
        print(f"Booking mail ok: {booking.id}")
        send_confirmation_email.apply_async(args=[name, email, package.name, total_price])
        generate_pdf_invoice.apply_async(args=[booking.id]) 
        return redirect(reverse('booking_success'))  # Replace 'success_page' with the actual URL name for the success page

    # If the request is GET, just render the page with the form
    return render(request, 'travel_package_booking.html', {'package': package})


def generate_flouci_payment(amount):
    # Replace with your actual values
    #app_token = "8d689544-f77b-43a7-94ab-93ef6b1e7104"
    #app_secret = "5727a53a-2033-41a4-839a-294c5e5ea299"
    
    payload = {
        "app_token": settings.FLOUCI_APP_TOKEN,
        "app_secret": settings.FLOUCI_APP_SECRET,
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


# Function to display recommended packages
def packages_recommendations(request):
    current_user = request.user  # Get current user
    
    # Get the latest booking for the user (assuming booking is associated with the user somehow)
    latest_booking = Booking.objects.filter(email=current_user.email).last()

    if not latest_booking:
        # If no booking is found, show general recommendations
        packages = TravelPackage.objects.all().order_by('-rating')[:3]  # Top 3 by rating
        return render(request, 'recommendations.html', {'packages': packages})
    
    # Extract user's preferences (rating from their last package)
    user_rating = latest_booking.package.rating
    user_price_preference = latest_booking.package.price  # Assuming this comes from the user's last booking
    user_destination_preference = latest_booking.package.destination  # Adjusted to 'destination'
    user_package_type_preference = latest_booking.package.package_type  # Example: 'Adventure', 'Beach', etc.
    
    # Now filter based on gender (if applicable)
    gender_preference = latest_booking.gender
    gender_based_filter = Q()
    if gender_preference == 'Male':
        gender_based_filter = Q(package_type__in=['Adventure', 'Beach', 'Cultural'])
    elif gender_preference == 'Female':
        gender_based_filter = Q(package_type__in=['Family', 'Relaxation', 'Cultural'])
    
    # Get the available packages based on gender
    recommendations = TravelPackage.objects.filter(gender_based_filter).order_by('-rating')
    
    # Function to create the feature vector for each package
    def get_feature_vector(pkg, user_rating):
        # Normalize the price (this is just an example, adjust to your data range)
        normalized_price = (pkg.price - min_price) / (max_price - min_price)  # Normalize between 0 and 1
        
        # Package type one-hot encoding
        package_types = ['Adventure', 'Beach', 'Cultural', 'Family', 'Relaxation']
        package_type_vector = [1 if pkg.package_type == pt else 0 for pt in package_types]
        
        # Destination one-hot encoding (you may want to adjust this depending on your destinations)
        destinations = ['Europe', 'Asia', 'Africa', 'America']
        destination_vector = [1 if pkg.destination == dest else 0 for dest in destinations]
        
        # Create the feature vector (combine all features into one vector)
        feature_vector = np.array([pkg.rating, normalized_price] + package_type_vector + destination_vector)
        
        # Create a feature vector for the user
        user_feature_vector = np.array([user_rating, user_price_preference] + [1 if user_package_type_preference == pt else 0 for pt in package_types] + [1 if user_destination_preference == dest else 0 for dest in destinations])
        
        return feature_vector, user_feature_vector

    # Get min and max prices for normalization
    min_price = min(pkg.price for pkg in recommendations)
    max_price = max(pkg.price for pkg in recommendations)
    
    # Calculate cosine similarity for each package manually
    similarities = []
    for pkg in recommendations:
        pkg_feature_vector, user_feature_vector = get_feature_vector(pkg, user_rating)
        
        # Calculate cosine similarity manually
        cosine_sim = np.dot(pkg_feature_vector, user_feature_vector) / (np.linalg.norm(pkg_feature_vector) * np.linalg.norm(user_feature_vector))
        similarities.append((pkg, cosine_sim))
    
    # Sort packages by similarity and return top 3
    sorted_recommendations = sorted(similarities, key=lambda x: x[1], reverse=True)[:3]
    top_recommendations = [pkg for pkg, similarity in sorted_recommendations]
    
    # Return the top 3 recommended packages
    return render(request, 'recommendations.html', {'packages': top_recommendations})


def booking_success(request):
    return render(request, 'booking_success.html')  # success.html is the success page template


def booking_fail(request):
    return render(request, 'booking_fail.html')  # success.html is the success page template


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
 