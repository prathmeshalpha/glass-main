from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
from django.core.validators import FileExtensionValidator

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Property(models.Model):
    property_name = models.CharField(max_length=255)
    post_type = models.CharField(max_length=10)
    property_type1 = models.CharField(max_length=15)
    specific_type1 = models.CharField(max_length=20, null=True, blank=True)
    specific_type2 = models.CharField(max_length=20, null=True, blank=True)
    maharera_number = models.CharField(max_length=50, blank=True, null=True)
    property_price = models.DecimalField(max_digits=12, decimal_places=2)
    property_area = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField(null=True, blank=True)
    balconies = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    ownership = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    address = models.TextField(max_length=500)
    appartment = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=10)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    floor_plan = models.TextField(max_length=3000,null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png','jpeg'])])  # Store paths of images as comma-separated values
    images = models.TextField(max_length=3000,null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png','jpeg'])])  # Store paths of images as comma-separated values
    videos = models.TextField(max_length=3000,null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov'])])  # Store paths of videos as comma-separated values
    
    # Feature columns as individual boolean fields
    security = models.BooleanField(default=False)
    powerbackup = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    ac = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    club = models.BooleanField(default=False)
    
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.property_type1} - {self.city} ({self.post_type})"
