from rest_framework import generics, permissions, filters, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.response import Response
from .models import Listing
from django.urls import reverse
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from django.conf import settings
from users.serializers import UserProfileSerializer
from listings.models import Listing, Inquiry
from .serializers import ListingSerializer, InquirySerializer
from .user_serializers import MyTokenObtainPairSerializer
from rest_framework.exceptions import ValidationError

User = get_user_model()

# --------------------------
# TEST CREATE LISTING (DEBUG)
# --------------------------
@api_view(['POST'])
def test_create_listing(request):
    try:
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')

        if not title or not description or not price:
            raise ValueError("title, description, and price are required")

        listing = Listing.objects.create(
            title=title,
            description=description,
            price=price,
            user=request.user if request.user.is_authenticated else None
        )

        return Response({"message": "Listing created", "id": listing.id})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --------------------------
# USER REGISTER VIEW
# --------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        try:
            send_mail(
                subject='Welcome to Real Estate App',
                message=f'Hi {user.username}, welcome to our Real Estate App!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception:
            pass

# --------------------------
# LISTINGS
# --------------------------
class ListingListCreateView(generics.ListCreateAPIView):
    queryset = Listing.objects.filter(published=True, purchased=False)
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'category']
    ordering_fields = ['price']

    def get_queryset(self):
        return Listing.objects.filter(published=True, purchased=False)

    def perform_create(self, serializer):
        user = self.request.user
        if not user or user.is_anonymous:
            raise ValidationError({"error": "Authentication required to create a listing."})
        serializer.save(user=user)


class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# --------------------------
# INQUIRIES
# --------------------------
class InquiryListCreateView(generics.ListCreateAPIView):
    serializer_class = InquirySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        listing_id = self.kwargs.get('pk')
        if not Listing.objects.filter(pk=listing_id).exists():
            raise NotFound("Listing not found.")
        return Inquiry.objects.filter(listing_id=listing_id)

    def perform_create(self, serializer):
        listing_id = self.kwargs.get('pk')
        listing = get_object_or_404(Listing, pk=listing_id)
        user = self.request.user if self.request.user.is_authenticated else None

        # Save the inquiry and get the instance
        inquiry = serializer.save(user=user, listing=listing)

        # Build listing URL
        listing_url = self.request.build_absolute_uri(f'/listing/{listing.id}/')

        # Send email to listing owner (agent)
        agent_email = listing.user.email
        try:
            send_mail(
                subject=f"New inquiry for {listing.title}",
                message=(
                    f"From: {inquiry.name} ({inquiry.email})\n\n"
                    f"{inquiry.message}\n\n"
                    f"View listing: {listing_url}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[agent_email],
                fail_silently=True,
            )
        except Exception:
            pass

        return inquiry

# --------------------------
# USER PROFILE
# --------------------------
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# --------------------------
# JWT TOKEN
# --------------------------
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# --------------------------
# PAYMENTS
# --------------------------
class PaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        listing = get_object_or_404(Listing, pk=pk, published=True, purchased=False)

        payment_success = True  # Stubbed for now
        if payment_success:
            listing.purchased = True
            listing.save()
            return Response(
                {"message": f"Payment successful! Listing '{listing.title}' is now marked as purchased."},
                status=status.HTTP_200_OK
            )

        return Response({"error": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)