from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/applicant/', views.complete_applicant_profile, name='complete_applicant_profile'),
    path('profile/employer/', views.complete_employer_profile, name='complete_employer_profile'),
    
    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_user_management, name='admin_user_management'),
    path('admin/users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('admin/users/<int:user_id>/toggle/', views.admin_toggle_user_active, name='admin_toggle_user_active'),
    path('admin/jobs/', views.admin_job_management, name='admin_job_management'),
    path('admin/jobs/<int:job_id>/<str:status>/', views.admin_update_job_status, name='admin_update_job_status'),
    path('admin/jobs/<int:job_id>/toggle/', views.admin_toggle_job_active, name='admin_toggle_job_active'),
    path('admin/applications/', views.admin_application_management, name='admin_application_management'),
    path('admin/stats/', views.admin_system_stats, name='admin_system_stats'),
]