from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from .serializers import MyTokenObtainPairSerializer, UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

# Register user
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Send welcome email
        send_mail(
            "Welcome to Real Estate App",
            f"Hello {user.username}, thank you for registering with us!",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
            )
            

# Profile view
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# JWT login
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer