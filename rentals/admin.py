
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Car, RentalOrder


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_customer', 'is_staff')  # Updated
    list_filter = ('is_customer', 'is_staff', 'is_superuser')  # Updated

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_customer', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_customer'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Car)
admin.site.register(RentalOrder)

