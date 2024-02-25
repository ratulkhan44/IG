# Django Imports
from django.contrib import admin

# Self Imports
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'mobile','is_active', 'created_at', 'updated_at']