# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # path('', landing_page, name='landing_page'),
    path('home/', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    
    path('login/', login_auth, name='login'),  # Assuming your login view is named login_auth
    path('logout/', logout_view, name='logout'),
    path('sign-up/', sign_up, name='sign-up'),
    path('update_profile/', update_profile, name='update_profile'),
    path('api/grades/<int:grade>/subjects/', get_subjects_for_grade, name='get_subjects_for_grade'),
    path('password-reset/', password_reset_request, name='password_reset_request'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset_password'),
    path('base', base, name="base"),
    path('user/subjects/', get_user_subjects_view, name='user-subjects')
]
    
    # Other URL patterns...
