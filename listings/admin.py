from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "user")  # ✅ all fields exist
    list_filter = ("price", "published", "purchased")  # ✅ safe filters
    search_fields = ("title", "description")  # ✅ text fields
    ordering = ("price",)  # newest first