from django.urls import path
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from . import views
from .views import InquiryListCreateView
from .views import PaymentView
from .views import test_create_listing
from .views import (
    MyTokenObtainPairView,
    UserProfileView,
    ListingListCreateView,
    ListingDetailView,
    test_create_listing,
    PaymentView,
)
from .auth_views import RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

# EMERGENCY RESET FUNCTION
def emergency_reset(request):
    User = get_user_model()
    u = User.objects.first()
    if not u:
        User.objects.create_superuser('admin2', 'admin2@gmail.com', 'Ikeja12345')
        return HttpResponse("CREATED -> Username: admin2 | Password: Ikeja12345 | Now go to /admin/")
    u.set_password('Ikeja12345')
    u.is_staff = True
    u.is_superuser = True
    u.save()
    return HttpResponse(f"RESET DONE -> Username: {u.username} | Password: Ikeja12345 | Now go to /admin/")

urlpatterns = [
    # Emergency reset - delete after use!
    path('reset-password-12345/', emergency_reset),
    
    # Authentication
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test-listing/', test_create_listing, name='test-listing'),
    path('listings/<int:pk>/inquiries/', InquiryListCreateView.as_view(), name='listing-inquiries'),
    path('test-create/', test_create_listing, name='test-create-listing'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('inquiries/', InquiryListCreateView.as_view(), name='inquiry-list'),
    path("listings/", views.ListingListCreateView.as_view(), name="listing-list-create"),
    path('listings/<int:pk>/pay/', PaymentView.as_view(), name='listing-payment'),
    path('listings/<int:pk>/payment/', PaymentView.as_view(), name='payment'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('listings/', views.ListingListCreateView.as_view(), name='listing-list'),
    path('api/listings/', ListingListCreateView.as_view(), name='listing-list'),
    path('api/listings/<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),
]