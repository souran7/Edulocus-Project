from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)  # Assuming mobile numbers as strings
    qualifications = models.CharField(max_length=200)
    experience = models.IntegerField(default=0)  # Assuming experience in years

    def __str__(self):
        return f"{self.first_name} {self.last_name}"