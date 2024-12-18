from django.conf import settings
from datetime import datetime, date
import uuid
import requests


def generate_flouci_payment(amount):
    """
    Generates a payment link for the user through the Flouci payment gateway.

    This function takes an amount, creates a payload with necessary payment details, 
    and makes a POST request to the Flouci API to generate a payment link. If the 
    API responds successfully, it returns the generated payment link, which the user 
    can use to complete the payment.

    Args:
        amount (Decimal): The total payment amount, which will be converted to cents.

    Returns:
        str or None: The payment link generated by the Flouci API if successful, 
        otherwise None if there is an error or the payment could not be generated.
    """
    payload = {
        "app_token": settings.FLOUCI_APP_TOKEN,
        "app_secret": settings.FLOUCI_APP_SECRET,
        "accept_card": "true",
        "amount": str(int(amount * 100)), 
        "success_link": "http://localhost:8000/packages/success/",
        "fail_link": "http://localhost:8000/packages/fail/",
        "session_timeout_secs": 1200, 
        "developer_tracking_id": str(uuid.uuid4()) 
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



def validate_booking(name, email, booking_date, num_adults, num_children, payment_method, consent):
    """
    Validates the booking form data to ensure it meets the necessary criteria.

    This function checks the following criteria for each of the form fields:
    - The name should be at least 2 characters long.
    - The email should contain an '@' symbol.
    - The booking date should be today or in the future.
    - The number of adults should be at least 1.
    - The number of children cannot be negative.
    - A payment method must be selected.
    - The user must agree to the terms and conditions.

    Args:
        name (str): The name of the person booking the package.
        email (str): The email address of the person making the booking.
        booking_date (str): The date of the booking (formatted as 'YYYY-MM-DD').
        num_adults (int): The number of adults in the booking.
        num_children (int): The number of children in the booking.
        payment_method (str): The chosen payment method.
        consent (str): User consent to the terms and conditions.

    Returns:
        dict: A dictionary of errors where the key is the field name and the value is the error message.
        If there are no errors, the dictionary will be empty.

    Example:
        errors = validate_booking('John Doe', 'john@example.com', '2024-12-25', 2, 1, 'Online', 'on')
        if errors:
            # Handle errors (e.g., show them to the user)
    """
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
    """
    Calculates the total price for a travel package based on the number of adults, children, 
    and a child discount.

    Args:
        package (TravelPackage): The travel package being booked.
        num_adults (int): Number of adults.
        num_children (int): Number of children.
        child_discount (Decimal): Discount for children (e.g., 0.5 for 50%).

    Returns:
        Decimal: The total price of the booking.

    Example:
        total_price = calculate_total_price(package, 2, 1, 0.5)
    """
    unit_price = package.price
    adults_price = unit_price * num_adults
    children_price = (unit_price * child_discount) * num_children
    return adults_price + children_price
