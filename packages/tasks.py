# Django Imports
from django.conf import settings
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib.auth.models import User

# Third-Party Imports
from weasyprint import HTML
import numpy as np
import os
import datetime

# Local Imports
from .models import Booking, TravelPackage
from celery import shared_task


@shared_task
def send_confirmation_email(name, email, package_name, total_price):
    """
    Sends a booking confirmation email to the user.

    This Celery task generates an email with the booking details and sends it 
    to the provided email address using Django's send_mail function.

    Args:
        name (str): The name of the person who made the booking.
        email (str): The email address to send the confirmation to.
        package_name (str): The name of the travel package booked.
        total_price (float): The total price of the booking.

    Returns:
        None: This function does not return a value. It sends an email asynchronously.
    
    Example:
        send_confirmation_email.apply_async(args=['John Doe', 'john@example.com', 'Beach Getaway', 499.99])
    """
    subject = f"Booking Confirmation for {package_name}"
    print('Sending email...')
    message = render_to_string('confirmation_email.html', {
        'name': name,
        'package_name': package_name,
        'total_price': total_price
    })
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=message  
    )


@shared_task
def generate_pdf_invoice(booking_id):
    """
    Generates a PDF invoice for a booking and stores it in the media directory.

    This Celery task retrieves the booking details from the database, calculates
    any applicable discounts, generates a PDF invoice using the data, and saves
    the invoice as a PDF file in the media directory under 'invoices'.

    Args:
        booking_id (int): The ID of the booking for which the invoice is generated.

    Returns:
        str: The filename of the saved PDF invoice.

    Example:
        generate_pdf_invoice.apply_async(args=[123])
    """
    booking = Booking.objects.get(id=booking_id)
    discount = (booking.package.price * 50 / 100) * booking.num_children
    today = datetime.date.today()
    print('Generating PDF invoice...')

    html_content = render_to_string('invoice.html', {'booking': booking, 'discount': discount, 'today': today})

    pdf = HTML(string=html_content).write_pdf()

    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'invoices'))
    filename = f'invoice_{booking.id}.pdf'
    pdf_file = ContentFile(pdf)  

    fs.save(filename, pdf_file)

    print(f'PDF invoice saved as {filename}')

    return filename


@shared_task
def package_recommendations(user_id):
    """
    Recommends travel packages for a user based on their previous booking preferences.

    This Celery task generates package recommendations for a user by analyzing their
    most recent booking details (rating, price, destination, and package type) and
    using a similarity-based approach to suggest packages that match their preferences.

    If no previous booking is found, general top-rated travel packages are recommended.
    The recommendations are filtered based on the user's gender and calculated using 
    cosine similarity between the user's preferences and available packages.

    Args:
        user_id (int): The ID of the user for whom the recommendations are generated.

    Returns:
        list: A list of IDs of the top 3 recommended travel packages.

    Example:
        package_recommendations.apply_async(args=[123])
    """
    current_user = User.objects.get(id=user_id)
    
    latest_booking = Booking.objects.filter(email=current_user.email).last()

    if not latest_booking:
        packages = TravelPackage.objects.all().order_by('-rating')[:3]  
        return [pkg.id for pkg in packages]
    
    user_rating = latest_booking.package.rating
    user_price_preference = latest_booking.package.price  
    user_destination_preference = latest_booking.package.destination  
    user_package_type_preference = latest_booking.package.package_type 
    
    gender_preference = latest_booking.gender
    gender_based_filter = Q()
    if gender_preference == 'Male':
        gender_based_filter = Q(package_type__in=['Adventure', 'Beach', 'Cultural'])
    elif gender_preference == 'Female':
        gender_based_filter = Q(package_type__in=['Family', 'Relaxation', 'Cultural'])
    
    recommendations = TravelPackage.objects.filter(gender_based_filter).order_by('-rating')

    min_price = min(pkg.price for pkg in recommendations)
    max_price = max(pkg.price for pkg in recommendations)
    
    def get_feature_vector(pkg, user_rating):
        normalized_price = (pkg.price - min_price) / (max_price - min_price)  
        
        package_types = ['Adventure', 'Beach', 'Cultural', 'Family', 'Relaxation']
        package_type_vector = [1 if pkg.package_type == pt else 0 for pt in package_types]
        
        destinations = ['Europe', 'Asia', 'Africa', 'America']
        destination_vector = [1 if pkg.destination == dest else 0 for dest in destinations]
        
        feature_vector = np.array([pkg.rating, normalized_price] + package_type_vector + destination_vector)
        user_feature_vector = np.array([user_rating, user_price_preference] + [1 if user_package_type_preference == pt else 0 for pt in package_types] + [1 if user_destination_preference == dest else 0 for dest in destinations])
        
        return feature_vector, user_feature_vector

    similarities = []
    for pkg in recommendations:
        pkg_feature_vector, user_feature_vector = get_feature_vector(pkg, user_rating)
        cosine_sim = np.dot(pkg_feature_vector, user_feature_vector) / (np.linalg.norm(pkg_feature_vector) * np.linalg.norm(user_feature_vector))
        similarities.append((pkg, cosine_sim))
    
    sorted_recommendations = sorted(similarities, key=lambda x: x[1], reverse=True)[:3]
    top_recommendations = [pkg for pkg, similarity in sorted_recommendations]
    
    return [pkg.id for pkg in top_recommendations]



