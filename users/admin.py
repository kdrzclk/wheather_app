from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'user_is_active', 'is_superuser')
    list_filter = ('email', 'is_staff', 'user_is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields':('email', 'password')}),
        ('Personel Info', {'fields':(
           'first_name', 'last_name', 'user_is_active')}),
        ('Permissions', {'fields':('groups',
        'user_permissions', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'user_is_active', 'is_superuser')
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, CustomUserAdmin)



