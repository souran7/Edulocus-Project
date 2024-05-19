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
    subjects = models.ManyToManyField('Subject', through='StudentSubject')

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

class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['student', 'subject']