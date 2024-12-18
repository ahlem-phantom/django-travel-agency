from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
from django.core.files.storage import FileSystemStorage
from .models import Booking
import os
from django.core.files.base import ContentFile
import datetime

# Task to send the confirmation email
@shared_task
def send_confirmation_email(name, email, package_name, total_price):
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
        html_message=message  # This ensures the email is sent as HTML
    )

# Task to generate PDF invoice
@shared_task
def generate_pdf_invoice(booking_id):
    booking = Booking.objects.get(id=booking_id)
    discount = (booking.package.price * 50 / 100) * booking.num_children
    today = datetime.date.today()
    print('Generating PDF invoice...')

    # Render invoice HTML template
    html_content = render_to_string('invoice.html', {'booking': booking, 'discount': discount, 'today': today})

    # Generate PDF from HTML
    pdf = HTML(string=html_content).write_pdf()

    # Store the PDF file using FileSystemStorage
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'invoices'))
    filename = f'invoice_{booking.id}.pdf'
    pdf_file = ContentFile(pdf)  # Wrap bytes into a file-like object

    fs.save(filename, pdf_file)

    print(f'PDF invoice saved as {filename}')

    return filename


@shared_task
def top_recommendations(user_id):
    current_user = User.objects.get(id=user_id)  # Get current user
    
    # Get the latest booking for the user
    latest_booking = Booking.objects.filter(email=current_user.email).last()

    if not latest_booking:
        # If no booking is found, show general recommendations
        packages = TravelPackage.objects.all().order_by('-rating')[:3]  # Top 3 by rating
        return [pkg.id for pkg in packages]
    
    # Extract user's preferences (rating from their last package)
    user_rating = latest_booking.package.rating
    user_price_preference = latest_booking.package.price  # Assuming this comes from the user's last booking
    user_destination_preference = latest_booking.package.destination  # Adjusted to 'destination'
    user_package_type_preference = latest_booking.package.package_type  # Example: 'Adventure', 'Beach', etc.
    
    # Gender-based package filter
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
        normalized_price = (pkg.price - min_price) / (max_price - min_price)  # Normalize between 0 and 1
        
        # Package type one-hot encoding
        package_types = ['Adventure', 'Beach', 'Cultural', 'Family', 'Relaxation']
        package_type_vector = [1 if pkg.package_type == pt else 0 for pt in package_types]
        
        # Destination one-hot encoding
        destinations = ['Europe', 'Asia', 'Africa', 'America']
        destination_vector = [1 if pkg.destination == dest else 0 for dest in destinations]
        
        # Create the feature vector
        feature_vector = np.array([pkg.rating, normalized_price] + package_type_vector + destination_vector)
        user_feature_vector = np.array([user_rating, user_price_preference] + [1 if user_package_type_preference == pt else 0 for pt in package_types] + [1 if user_destination_preference == dest else 0 for dest in destinations])
        
        return feature_vector, user_feature_vector

    # Get min and max prices for normalization
    min_price = min(pkg.price for pkg in recommendations)
    max_price = max(pkg.price for pkg in recommendations)
    
    # Calculate cosine similarity for each package manually
    similarities = []
    for pkg in recommendations:
        pkg_feature_vector, user_feature_vector = get_feature_vector(pkg, user_rating)
        cosine_sim = np.dot(pkg_feature_vector, user_feature_vector) / (np.linalg.norm(pkg_feature_vector) * np.linalg.norm(user_feature_vector))
        similarities.append((pkg, cosine_sim))
    
    # Sort packages by similarity and return top 3
    sorted_recommendations = sorted(similarities, key=lambda x: x[1], reverse=True)[:3]
    top_recommendations = [pkg for pkg, similarity in sorted_recommendations]
    
    return [pkg.id for pkg in top_recommendations]  # Return the IDs of recommended packages