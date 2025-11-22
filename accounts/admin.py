from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ApplicantProfile, EmployerProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(ApplicantProfile)
admin.site.register(EmployerProfile)