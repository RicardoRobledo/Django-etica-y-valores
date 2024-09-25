from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserModel, UserLevelCategory


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserModel


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    # Make the date fields and last_login read-only
    readonly_fields = ('last_login', 'created_at', 'updated_at')

    fieldsets = (
        # For the username and password fields
        (None, {'fields': ('username', 'password')}),
        # User's personal information
        ('Personal info', {'fields': ('first_name',
         'middle_name', 'last_name', 'email')}),
        # Permissions and groups
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser',
         'groups', 'user_permissions')}),
        # Important dates, read-only
        ('Important dates', {
         'fields': ('last_login', 'created_at', 'updated_at')}),
        # Custom fields from the UserModel
        ('Other', {'fields': ('user_level_id', 'supervisor', 'enterprise_id')}),
    )

    add_fieldsets = (
        # Basic fields in the add user form
        (None, {'fields': ('username', 'password1', 'password2', )}),
        # Personal info section in the add form
        ('Personal info', {'fields': ('first_name',
         'middle_name', 'last_name', 'email')}),
        # Permissions in the add form
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser',
         'groups', 'user_permissions')}),
        # Custom fields in the add user form
        ('Other', {'fields': ('user_level_id', 'supervisor', 'enterprise_id')}),
    )

    # Allow search by these fields
    search_fields = ('email', 'username', 'first_name', 'last_name')
    # Order by email
    ordering = ('email',)
    # Use horizontal widget for groups and permissions
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(UserModel, UserAdmin)
admin.site.register(UserLevelCategory)
