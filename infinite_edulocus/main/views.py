from django.shortcuts import render
from django.db.models import Max
from django.core.paginator import Paginator
from django.template.defaulttags import register
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import login_required
from .forms import  LoginForm,PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from edulocus.settings import LOGIN_URL
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.utils.encoding import force_str
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import *
import re
import random
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from .forms import NewPasswordForm
from django.http import JsonResponse
import json
from django.db import transaction
from .mailers import send_welcome_email








def login_auth(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect to home page if user is already logged in

    if request.method == 'POST':
        email = request.POST.get('email')
        provided_password = request.POST.get('password')
        default_password = "Password"  # Replace with your actual default password
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('login')
        
        # Attempt to authenticate with the provided password
        user = authenticate(request, username=user.username, password=provided_password)

        # If authentication with the provided password fails, try the default password
        if user is None and provided_password == default_password:
            try:
                user = User.objects.get(username=user.username)
                # Log in the user without calling authenticate (use with caution)
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
            except User.DoesNotExist:
                messages.error(request, 'User does not exist')
                return redirect('login')

        if user is not None:
            # Authentication with the provided password succeeded
            login(request, user)
            return redirect('dashboard')  # Redirect to home page after successful login

        # Authentication failed with both the provided and default passwords
        messages.error(request, 'Email or Password Incorrect')
        return redirect('login')

    return render(request, 'login.html', context={'login_form': LoginForm(request.POST)})

def logout_view(request):
    logout(request)
    return redirect('login') 



def create_unique_username(first_name):
    # Generate a random 4-5 digit number
    random_digits = str(random.randint(10000, 99999))
    
    # Concatenate first_name with random digits
    username = first_name.lower() + random_digits

    # Check if the username already exists
    while User.objects.filter(username=username).exists():
        random_digits = str(random.randint(10000, 99999))
        username = first_name.lower() + random_digits

    return username


@csrf_exempt
def sign_up(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))  # Redirect to dashboard if user is already logged in

    error_message = None

    if request.method == 'POST':
        try:
            # Retrieve data from POST request
            user_type = request.POST.get('user_type')
            first_name = request.POST.get('first_name').strip()  # Remove leading/trailing whitespaces
            last_name = request.POST.get('last_name').strip()  # Remove leading/trailing whitespaces
            email = request.POST.get('email').strip()  # Remove leading/trailing whitespaces
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            mobile_number = request.POST.get('mobile_number').strip()  # Remove leading/trailing whitespaces

            # Validate and sanitize email
            validate_email(email)

            # Validate mobile number
            if not re.match(r'^\+?\d{10,15}$', mobile_number):
                raise ValidationError('Invalid mobile number format')

            # Validate password and confirm_password match
            if password != confirm_password:
                raise ValidationError("Passwords do not match")

            if len(password) < 8:
                raise ValidationError("Password must be at least 8 characters long")

            if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}|:"<>?`~])', password):
                raise ValidationError("Password must contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character")

            # Validate first name and last name (alphabets only)
            if not first_name.isalpha() or not last_name.isalpha():
                raise ValidationError("First name and last name should contain alphabets only")

            # Check if a user with the provided email already exists
            if User.objects.filter(email=email).exists():
                raise ValidationError('User with this email already exists')

            # Create a new user
            unique_username = create_unique_username(first_name)
            user = User.objects.create_user(username=unique_username, email=email, password=password, first_name=first_name, last_name=last_name)

            # Create a profile for the user
            profile = Profile.objects.create(
                user=user,
                user_type=user_type,
                email=email,
                mobile_number=mobile_number,
                first_name=first_name, 
                last_name=last_name
            )

            # Log in the user after successful registration
            login(request, user)
            # Send welcome email
            send_welcome_email(email)
            return HttpResponseRedirect(reverse('dashboard'))  # Redirect to dashboard after successful registration

        except ValidationError as e:
            # Handle validation errors
            error_message = str(e)

        except Exception as e:
            # Handle other exceptions
            error_message = str(e)

    return render(request, 'sign_up.html', {'error': error_message})

@login_required(login_url=LOGIN_URL)
def dashboard(request):
    # Get the logged-in user's profile
    user_profile = Profile.objects.get(user=request.user)

    # Query all grades
    grades = Grade.objects.all().values_list('grade', flat=True).distinct()

    # Initialize variables to store grade and subjects for students
    student_grade = None
    student_subjects = None

    # Check if the user is a student
    

    # Check if the user is a superuser
    if request.user.is_superuser:
        show_modal = False  # Ignore show_modal for superusers
    else:
        # Check if the user's basic details are false
        show_modal = not user_profile.basic_details

    # if user_profile.user_type == 'Student':
    #     # Get the student instance
    #     student_instance = Student.objects.get(profile=user_profile)
        
    #     # Retrieve the grade chosen by the student
    #     student_grade = student_instance.grade
        
    #     # Retrieve the subjects chosen by the student
    #     student_subjects = student_instance.subjects.all()    

    # Pass the show_modal flag, user_profile, grades, student_grade, and student_subjects to the template
    return render(request, 'dashboard.html', {'show_modal': show_modal, 'user_profile': user_profile, 'grades': grades, 'student_grade': student_grade, 'student_subjects': student_subjects})

def get_subjects_for_grade(request, grade):
    # Query the Grade object for the specified grade
    try:
        grade_obj = Grade.objects.get(grade=grade)
    except Grade.DoesNotExist:
        return JsonResponse({'error': 'Grade not found'}, status=404)

    # Get the subjects associated with the grade
    subjects = grade_obj.subjects.all()

    # Serialize subjects data
    subjects_data = [{'id': subject.id, 'name': subject.name} for subject in subjects]

    # Return JSON response with subjects data
    return JsonResponse(subjects_data, safe=False)
@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        # Extract form data from JSON payload
        data = json.loads(request.body)
        dob = data.get('dob')
        gender = data.get('gender')
        qualifications = data.get('qualifications')
        experience = data.get('experience')
        grades = data.get('grades')  # Assuming this is sent from the frontend
        subjects = data.get('subjects')  # Assuming this is sent from the frontend

        # Get the user's profile
        user_profile = request.user.profile

        # Update profile information
        user_profile.date_of_birth = dob
        user_profile.gender = gender
        user_profile.basic_details = True
        user_profile.save()

        # Check if user is a student
        if user_profile.user_type == 'Student':
            # Create Student object
            student_instance = Student.objects.create(profile=user_profile, grade=grades)

            # Add selected subjects to the student
            if subjects:
                subjects_instances = Subject.objects.filter(id__in=subjects)
                student_instance.subjects.add(*subjects_instances)  # Add subjects to the M2M relation

        # Check if user is a teacher
        elif user_profile.user_type == 'Teacher':
            # Create Teacher object
            teacher_profile = Teacher.objects.create(profile=user_profile, qualifications=qualifications, experience=experience)

        return JsonResponse({'message': 'Profile updated successfully'}, status=200)

    # Return error response if request method is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=405)



















def send_password_reset_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = request.build_absolute_uri('/reset-password/{}/{}'.format(uid, token))

    email_subject = 'Password Reset'
    email_body = render_to_string('email/password_reset_email.html', {
        'reset_link': reset_link,
    })

    send_mail(email_subject, email_body, 'infiniteedulocus@gmail.com', [user.email])




def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                send_password_reset_email(request, user)
                messages.success(request, 'An email has been sent with instructions to reset your password.')
            except User.DoesNotExist:
                messages.error(request, 'Email does not exist.')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = NewPasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                confirm_password = form.cleaned_data['confirm_password']
                if password == confirm_password:
                    user.set_password(password)
                    user.save()
                    update_session_auth_hash(request, user)  # Update session to prevent logout
                    messages.success(request, 'Your password has been reset successfully.')
                    return redirect('login')
                else:
                    messages.error(request, 'Passwords do not match.')
        else:
            form = NewPasswordForm()
        return render(request, 'reset_password.html', {'form': form})
    else:
        messages.error(request, 'Invalid reset link.')
        return redirect('login')



@login_required(login_url=LOGIN_URL)
def home(request):
    return render(request, 'home.html')


def landing_page(request):
    return render(request, 'index.html')




def base(request):
    return render(request, 'base.html')