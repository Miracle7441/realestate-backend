from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "email", "phone_number", "is_staff", "is_active")
    search_fields = ("username", "email", "phone_number")
    ordering = ("id",)

    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("phone_number", "profile_picture")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("phone_number", "profile_picture")}),
    )
