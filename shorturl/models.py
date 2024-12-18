from django.db import models
from django.contrib.auth.models import User

class ShortLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.PositiveIntegerField(default=0)  # Счётчик переходов

    def __str__(self):
        return self.short_code

class ClickStats(models.Model):
    short_link = models.ForeignKey(ShortLink, on_delete=models.CASCADE, related_name='click_stats')
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    clicked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_link.short_code} - {self.country}, {self.city} - {self.clicked_at}"