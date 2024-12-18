from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.urls import reverse

from .models import TravelPackage, Booking
from .forms import TravelPackageForm
from .tasks import generate_pdf_invoice, send_confirmation_email, package_recommendations
from .utils import validate_booking, calculate_total_price, generate_flouci_payment

from decimal import Decimal
from datetime import datetime


def book_package(request, pk):
    """
    Renders the booking page for a specific travel package.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The ID of the travel package to book.

    Returns:
        HttpResponse: The rendered booking page for the package.
    """
    package = get_object_or_404(TravelPackage, pk=pk)
    return render(request, 'travel_package_booking.html', {'package': package})


def travel_package_list(request):
    """
    Renders a list of all travel packages along with rating options.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered list page displaying all travel packages and rating options.
    """
    travel_packages =  TravelPackage.objects.all()
    ratings_range = range(1, 6)  # Range for star rating
    return render(request, 'travel_package_list.html', {'packages': travel_packages, 'ratings_range': ratings_range}) 


def booking_handler_view(request, package_id):
    """
    Handles the booking process for a travel package, including form validation, 
    price calculation, payment handling, and booking confirmation.

    Args:
        request (HttpRequest): The HTTP request object.
        package_id (int): The ID of the travel package being booked.

    Returns:
        HttpResponse: Redirects to payment URL if online payment is selected, 
                       or to success/failure pages based on the booking outcome.
    """
    package = get_object_or_404(TravelPackage, id=package_id)
    child_discount = Decimal('0.5')

    if request.method == 'POST':
        # Fetch form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        booking_date = request.POST.get('datetime')
        num_adults = int(request.POST.get('SelectPerson', 0))
        num_children = int(request.POST.get('SelectKids', 0))
        gender = request.POST.get('SelectGender', 'None')  
        payment_method = request.POST.get('payment_method', '0') 
        consent = request.POST.get('consent')

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
                # If the payment URL could not be generated, return error page
                booking.delete()
                return redirect(reverse('booking_fail'))
        

        print(f"Booking mail ok: {booking.id}")
        send_confirmation_email.apply_async(args=[name, email, package.name, total_price])
        generate_pdf_invoice.apply_async(args=[booking.id]) 
        return redirect(reverse('booking_success'))  

    return render(request, 'travel_package_booking.html', {'package': package})


def packages_recommendations(request):
    """
    Handles the generation of personalized travel package recommendations 
    for the current user based on their past bookings.

    Args:
        request (HttpRequest): The HTTP request object containing the current user.

    Returns:
        HttpResponse: Renders the 'recommendations.html' template with the recommended travel packages.
    """
    result=package_recommendations.apply_async(args=[request.user.id])
    recommended_package_ids = result.get()  
    top_recommendations = TravelPackage.objects.filter(id__in=recommended_package_ids)
    return render(request, 'recommendations.html', {'packages': top_recommendations})


def booking_success(request):
    """
    Renders the booking success page after a successful booking.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'booking_success.html' template to show the user the booking confirmation.
    """
    return render(request, 'booking_success.html') 


def booking_fail(request):
    """
    Renders the booking failure page when a booking attempt fails.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'booking_fail.html' template to inform the user of a failed booking.
    """
    return render(request, 'booking_fail.html')  



 