from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User




class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

 

class Property(models.Model):
    property_name = models.CharField(max_length=255)
    post_type = models.CharField(max_length=10)
    property_type1 = models.CharField(max_length=15)
    specific_type1 = models.CharField(max_length=20, null=True, blank=True)
    
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
 # Store paths of videos as comma-separated values
    
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
    approved = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.property_type1} - {self.city} ({self.post_type})"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property.property_name}"
    
class PropertyVideo(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='property_videos/')

    def __str__(self):
        return f"Video for {self.property.property_name}"
    
class PropertyFloorPlan(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='floor_plans')
    floor_plan = models.FileField(upload_to='property_floor_plan/')

    def __str__(self):
        return f"Image for {self.property.property_name}"
    
    
