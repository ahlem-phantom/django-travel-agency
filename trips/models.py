from django.db import models

class TravelPackage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.JSONField()  # Example: {"adventure": 5, "luxury": 2, "family_friendly": 3}
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="packages/", null=True, blank=True)

    def __str__(self):
        return self.title
