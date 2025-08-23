from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Listing(models.Model):
    CATEGORY_CHOICES = [
        ("house", "House"),
        ("apartment", "Apartment"),
        ("land", "Land"),
        ("duplex", "Duplex"),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings"
    )
    published = models.BooleanField(default=True)
    purchased = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.title


class Inquiry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
    null=True,
    blank=True
    )
    message = models.TextField()
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="inquiries"
        
    )
    def _str_(self):
        return f"Inquiry from {self.name} about {self.listing.title}"