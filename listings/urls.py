from django.urls import path
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

urlpatterns = [
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
 # User Profile
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
 # Listings
     path('listings/', views.ListingListCreateView.as_view(), name='listing-list'),
     path('api/listings/', ListingListCreateView.as_view(), name='listing-list'),
     path('api/listings/<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),
]