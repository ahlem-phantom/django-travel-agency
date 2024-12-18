from django.db import models

class TravelNews(models.Model):
    '''
    Model for Travel News
    '''
    title = models.CharField(max_length=255)
    link = models.URLField()
    content = models.TextField(blank=True)
    published_date = models.DateField(blank=True, null=True)  # Change to DateField or DateTimeField
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    read_time = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return  self.title
    




