# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('home/', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    
    path('login/', login_auth, name='login'),  # Assuming your login view is named login_auth
    path('logout/', logout_view, name='logout'),
    path('sign-up/', sign_up, name='sign-up'),
    path('password-reset/', password_reset_request, name='password_reset_request'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset_password'),
    path('base', base, name="base")
    
    # Other URL patterns...
]