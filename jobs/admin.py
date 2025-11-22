from django.contrib import admin
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'category', 'location', 'job_type', 'status', 'is_active', 'created_at']
    list_filter = ['status', 'is_active', 'job_type', 'category', 'created_at']
    search_fields = ['title', 'employer__company_name', 'location', 'category']
    list_editable = ['status', 'is_active']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_date']
    list_filter = ['status', 'applied_date']
    search_fields = ['applicant__full_name', 'job__title', 'job__category']
    list_editable = ['status']
    readonly_fields = ['applied_date', 'updated_at']