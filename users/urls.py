from django.urls import path
from .views import RegisterView, UserProfileView, MyTokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
]