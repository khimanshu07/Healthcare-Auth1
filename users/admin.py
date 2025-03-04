from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Specialty

class CustomUserAdmin(UserAdmin):
    # Define the fields to display in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'get_specialties')
    
    filter_horizontal = ('specialties',)

    # Add filters for user_type and is_staff
    list_filter = ('user_type', 'is_staff')

    # Define the fieldsets for the add/edit user page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'user_type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Address', {'fields': ('address_line1', 'city', 'state', 'pincode')}),
        ('Profile Picture', {'fields': ('profile_picture',)}),
        ('Specialties', {'fields': ('specialties',)}),  # Add specialties field
    )

    # Define the fieldsets for the add user page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'is_staff'),
        }),
    )

    # Custom method to display specialties in the list view
    def get_specialties(self, obj):
        return ", ".join([s.name for s in obj.specialties.all()])
    get_specialties.short_description = 'Specialties'

# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)

# Register the Specialty model
admin.site.register(Specialty)