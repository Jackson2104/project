from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Announcement
from django import forms
 

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'f_name', 'l_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')  # 🔥 Ongeza role hapa
    ordering = ('email',)
    search_fields = ('email', 'f_name', 'l_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('f_name', 'm_name', 'l_name', 'location', 'date_of_birth', 'phone_no', 'role')}),  # 🔥 role hapa
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'f_name', 'm_name', 'l_name',
                'location', 'date_of_birth', 'phone_no',
                'role',  # 🔥 Hapa pia
                'password1', 'password2',
                'is_staff', 'is_active'
            ),
        }),
    )
 

admin.site.register(CustomUser, CustomUserAdmin)

# Register Announcement
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)

