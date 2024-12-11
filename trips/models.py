from django.db import models

class TravelPackage(models.Model):
    FAMILY = 'Family'
    ADVENTURE = 'Adventure'
    ROMANTIC = 'Romantic'
    BUSINESS = 'Business'

    TAG_CHOICES = [
        (FAMILY, 'Family Trip'),
        (ADVENTURE, 'Adventure'),
        (ROMANTIC, 'Romantic Getaway'),
        (BUSINESS, 'Business Trip'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    tags = models.CharField(max_length=20, choices=TAG_CHOICES, default=FAMILY)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="packages/", null=True, blank=True)  # Ensure the upload path is correct
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    destination = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.title}, {self.description}, {self.tags}, {self.price}, {self.image.url if self.image else 'No Image'}, {self.start_date}, {self.end_date}, {self.destination}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5

    class Meta:
        unique_together = ('user', 'trip')  # A user can only rate a trip once
    
    def __str__(self):
        return f"{self.user.username} - {self.trip.title} - {self.rating}"