from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from jobs.models import Application

@login_required
def applicant_dashboard(request):
    if request.user.role != 'applicant':
        return redirect('home')
    
    try:
        applicant_profile = request.user.applicantprofile
        applications = Application.objects.filter(applicant=applicant_profile).select_related('job', 'job__employer')
        
        context = {
            'applicant_profile': applicant_profile,
            'applications': applications,
            'total_applications': applications.count(),
            'active_applications': applications.exclude(status__in=['rejected', 'hired']).count(),
        }
        return render(request, 'applicants/dashboard.html', context)
    
    except Exception as e:
        return redirect('complete_applicant_profile')

@login_required
def application_history(request):
    if request.user.role != 'applicant':
        return redirect('home')
    
    applicant_profile = request.user.applicantprofile
    applications = Application.objects.filter(applicant=applicant_profile).select_related('job', 'job__employer')
    
    context = {
        'applications': applications
    }
    return render(request, 'applicants/applications.html', context)