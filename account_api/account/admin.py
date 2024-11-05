from django.contrib import admin
from .models import CustomUser, Profile

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'username',
        'email',
        'phone_number',
        'is_active',
        'is_staff'
    ]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'profile_image',
        'bio',
        'url',
        'created_at'
    ]

