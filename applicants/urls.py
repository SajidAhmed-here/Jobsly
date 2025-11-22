from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('applications/', views.application_history, name='application_history'),
]