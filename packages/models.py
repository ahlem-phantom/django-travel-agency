from django.db import models

class TravelPackage(models.Model):
    # Fields to match the travel package data
    name = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    package_type = models.CharField(max_length=50, choices=[
        ('Beach', 'Beach'),
        ('Adventure', 'Adventure'),
        ('Cultural', 'Cultural'),
        ('Family', 'Family'),
        ('Relaxation', 'Relaxation'),
        ('City', 'City'),
    ])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)  # e.g., '7 days'
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # Rating out of 5
    description = models.TextField()
    available = models.BooleanField(default=True)  # To mark availability
    tags = models.ManyToManyField('Tag', related_name='travel_packages', blank=True)
    image = models.ImageField(upload_to="packages/", null=True, blank=True)  # Ensure the upload path is correct

    def __str__(self):
        return self.name 


class Booking(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    gender = models.CharField(
        max_length=50,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('None', 'None')],
        default='None'  # Default value for existing rows
    )
    datetime = models.DateTimeField()
    num_adults = models.PositiveIntegerField(default=0)  # Default to 0
    num_children = models.PositiveIntegerField(default=0)  # Default to 0
    payment_method = models.CharField(
        max_length=50,
        choices=[('Online', 'Online'), ('On Site', 'On Site')],
        default='None'  # Default value for existing rows
    )
    package = models.ForeignKey('TravelPackage', on_delete=models.CASCADE, related_name='bookings')
    payment_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending' )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Booking by {self.name} for {self.package.name}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

