from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Listing, Inquiry

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_agent', 'is_buyer']
        read_only_fields = ['id', 'username', 'is_agent', 'is_buyer']

class ListingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # shows username instead of user ID
    class Meta:
        model = Listing
        fields = "__all__"
        read_only_fields = ['user', 'created_at', 'updated_at']

class PaymentSerializer(serializers.ModelSerializer):
    Listing_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

# ------------------------------
# Add InquirySerializer here
# ------------------------------
class InquirySerializer(serializers.ModelSerializer):
    listing = serializers.ReadOnlyField(source='user.username')  # optional, shows listing title
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Inquiry
        fields = ["id", "name", "email", "message", "user", "listing"]
        read_only_fields = ['user', 'id', 'listing']

    def validate_listing(self, value):
        """
        Ensure the listing exists and is valid.
        """
        if value is None:
            raise serializers.ValidationError("You must provide a listing ID.")
        return value