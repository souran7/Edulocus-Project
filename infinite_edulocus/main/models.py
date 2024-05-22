from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('Admin', 'Admin'),
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)  # Assuming mobile numbers as strings
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    basic_details = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Student(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)
    grade = models.IntegerField(choices=[(i, i) for i in range(6, 13)])
    subjects = models.ManyToManyField('Subject',  null=True, blank=True)

    def __str__(self):
        return self.profile.user.username + "'s Student Profile"

class Teacher(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)
    experience = models.IntegerField()
    qualifications = models.TextField(blank=True, null=True)

class Grade(models.Model):
    grade = models.IntegerField(choices=[(i, i) for i in range(6, 13)])
    subjects = models.ManyToManyField('Subject')

    def __str__(self):
        subjects_list = ', '.join(str(subject) for subject in self.subjects.all())
        return f"Grade {self.grade} - Subjects: {subjects_list}"

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name






class Email_Body(models.Model):
    EMAIL_TYPES = (
        ('RESET_PASSWORD', 'RESET_PASSWORD'),
        ('FORGOT_PASSWORD', 'FORGOT_PASSWORD'),
        ('WELCOME_MAIL', 'WELCOME_MAIL'),
    
    )
    email_type = models.CharField(max_length=50, choices=EMAIL_TYPES)
    body =models.TextField(blank=True, null=True)
    subject =models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.email_type}"
    



class EmailLog(models.Model):
    EMAIL_STATUS = (
        ('SUCCESS', 'Success'),
        ('ERROR', 'Error'),
    )
    
    email_type = models.CharField(max_length=50, choices=Email_Body.EMAIL_TYPES)
    status = models.CharField(max_length=10, choices=EMAIL_STATUS)
    reason = models.TextField(blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    user_email = models.EmailField()

    def __str__(self):
        return f"{self.email_type} - {self.status} - {self.datetime}"