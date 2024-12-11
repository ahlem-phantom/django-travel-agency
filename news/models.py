from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_on = models.DateTimeField()

    def __str__(self):
        return self.title

class TravelNews(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    content = models.TextField(blank=True)
    published_date = models.DateField(blank=True, null=True)  # Change to DateField or DateTimeField
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    read_time = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return {self.title, self.published_date, self.category, self.read_time, self.image_url, self.link}
    




