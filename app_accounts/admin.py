from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Driver

# Custom User Admin
class UserAdmin(BaseUserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'user_type', 'password1', 'password2')}
        ),
    )
    list_display = ('username', 'email', 'phone_number', 'user_type', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('email',)

class DriverAdmin(admin.ModelAdmin):
    model = Driver
    list_display = ('user', 'gender', 'latitude', 'longitude', 'is_active', 'license', 'created_at', 'updated_at')
    search_fields = ('user__username', 'license')
    list_filter = ('is_active',)

# Your existing model admin configurations

admin.site.site_header = "RideFast Admin Panel"
admin.site.site_title = "RideFast Admin"
admin.site.index_title = "Welcome to RideFast Management"
admin.site.register(User, UserAdmin)
admin.site.register(Driver, DriverAdmin)