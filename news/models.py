from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_on = models.DateTimeField()

    def __str__(self):
        return self.title
