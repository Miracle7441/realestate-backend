from django.urls import path
from .views import (
    RegisterView,
     )
from django.urls import path 
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # User registration
    path('register/', RegisterView.as_view(), name='user-register'),
    
    # JWT login
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    ]