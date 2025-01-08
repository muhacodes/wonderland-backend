# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user accounts
    form = UserChangeForm
    add_form = UserCreationForm

    # Fields to display in the admin interface
    list_display = ('email',  'username', 'admin')
    list_filter = ('admin', 'staff', 'active')

    fieldsets = (
        (None, {'fields': ('email', 'password',  'username')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('admin', 'staff', 'active')}),
    )

    # Fields to use when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'admin', 'staff', 'active')}
        ),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()

# Unregister the Group model if you don't use it
admin.site.unregister(Group)

# Register your custom user model and admin class
admin.site.register(User, UserAdmin)