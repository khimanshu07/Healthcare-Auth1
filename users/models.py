from django.contrib.auth.models import AbstractUser
from django.db import models

class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    address_line1 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    specialties = models.ManyToManyField(Specialty, blank=True)  # Many-to-many relationship

    def is_doctor_without_specialty(self):
        """Check if the user is a doctor without any specialties."""
        return self.user_type == 'doctor' and not self.specialties.exists()