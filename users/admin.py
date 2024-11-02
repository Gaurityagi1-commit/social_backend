from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
    inlines = (UserProfileInline,)  # Add the UserProfile inline

    # You can keep the fieldsets for User model fields only
    fieldsets = BaseUserAdmin.fieldsets



# Register the new User admin
admin.site.register(User, CustomUserAdmin)