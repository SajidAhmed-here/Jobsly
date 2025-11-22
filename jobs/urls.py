from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('jobs/<int:job_id>/success/', views.application_success, name='application_success'),
    path('employer/jobs/post/', views.post_job, name='post_job'),
    path('employer/jobs/', views.manage_jobs, name='manage_jobs'),
    path('employer/jobs/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
    path('employer/applications/<int:application_id>/<str:status>/', 
         views.update_application_status, name='update_application_status'),
]