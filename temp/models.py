from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Property(models.Model):
    post_type = models.CharField(max_length=10)
    property_type1 = models.CharField(max_length=15)
    specific_type1 = models.CharField(max_length=20)
    specific_type2 = models.CharField(max_length=20)
    maharera_number = models.CharField(max_length=50, blank=True, null=True)
    property_price = models.DecimalField(max_digits=12, decimal_places=2)
    property_area = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField(null=True, blank=True)
    balconies = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    ownership = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    appartment = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    images = models.TextField(null=True, blank=True)  # Store paths of images as comma-separated values
    videos = models.TextField(null=True, blank=True)  # Store paths of videos as comma-separated values
    features = models.TextField(null=True, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property_type1} - {self.city} ({self.post_type})"