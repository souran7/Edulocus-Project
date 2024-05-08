# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('home/', home, name='home'),
    
    path('login/', login_auth, name='login'),  # Assuming your login view is named login_auth
    path('logout/', logout_view, name='logout'),
    # Other URL patterns...
]