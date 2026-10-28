from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def home(request):
    return HttpResponse("Welcome to the Real Estate API! Go to /admin/")

def create_admin(request):
    User = get_user_model()
    if not User.objects.filter(username="miracle").exists():
        User.objects.create_superuser("miracle", "", "Miracle123")
        return HttpResponse("Admin CREATED! Username: miracle Password: Miracle123")
    return HttpResponse("Admin already exists! Username: miracle Password: Miracle123")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.usersurls")),
    path("api/", include("listings.urls")),
    path("", home),
    path("api/", include("users.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
]