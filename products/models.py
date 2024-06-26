from django.db import models
from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "articles")
    image = models.ImageField(upload_to='images/', blank=True)
    price = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = "like_articles")
    def __str__(self):
        return self.title
    