from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Job, Application
from .forms import JobForm, ApplicationForm
from .filters import JobFilter
from accounts.models import ApplicantProfile, EmployerProfile

def home(request):
    latest_jobs = Job.objects.filter(status='approved', is_active=True).order_by('-created_at')[:8]
    
    # Get unique categories for the home page
    categories = Job.objects.filter(status='approved', is_active=True).values_list('category', flat=True).distinct()[:8]
    
    context = {
        'latest_jobs': latest_jobs,
        'categories': categories,
    }
    return render(request, 'jobs/home.html', context)

def job_list(request):
    jobs = Job.objects.filter(status='approved', is_active=True).order_by('-created_at')
    
    # Search functionality - FIXED SYNTAX
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(employer__company_name__icontains=query) |
            Q(location__icontains=query) |
            Q(category__icontains=query)
        )
    
    # Filter functionality
    job_filter = JobFilter(request.GET, queryset=jobs)
    filtered_jobs = job_filter.qs
    
    # Pagination
    paginator = Paginator(filtered_jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique categories for filter suggestions
    categories = Job.objects.filter(status='approved', is_active=True).values_list('category', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'filter': job_filter,
        'total_jobs': filtered_jobs.count(),
        'categories': categories,
    }
    return render(request, 'jobs/job_list.html', context)

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, status='approved', is_active=True)
    
    has_applied = False
    if request.user.is_authenticated and request.user.role == 'applicant':
        try:
            applicant_profile = request.user.applicantprofile
            has_applied = Application.objects.filter(job=job, applicant=applicant_profile).exists()
        except ApplicantProfile.DoesNotExist:
            pass
    
    context = {
        'job': job,
        'has_applied': has_applied
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
def apply_job(request, job_id):
    if request.user.role != 'applicant':
        messages.error(request, 'Only job seekers can apply for jobs.')
        return redirect('job_detail', job_id=job_id)
    
    job = get_object_or_404(Job, id=job_id, status='approved', is_active=True)
    applicant_profile = get_object_or_404(ApplicantProfile, user=request.user)
    
    # Check if already applied
    if Application.objects.filter(job=job, applicant=applicant_profile).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', job_id=job_id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = applicant_profile
            
            # Use applicant's default CV if not provided
            if not application.cv and applicant_profile.cv:
                application.cv = applicant_profile.cv
            
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('application_success', job_id=job_id)
    else:
        initial = {}
        if applicant_profile.cv:
            initial['cv'] = applicant_profile.cv
        form = ApplicationForm(initial=initial)
    
    context = {
        'form': form,
        'job': job
    }
    return render(request, 'jobs/apply_job.html', context)

@login_required
def application_success(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/application_success.html', {'job': job})

@login_required
def post_job(request):
    if request.user.role != 'employer':
        messages.error(request, 'Only employers can post jobs.')
        return redirect('home')
    
    employer_profile = get_object_or_404(EmployerProfile, user=request.user)
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer_profile
            job.save()
            
            messages.success(request, 'Job posted successfully! It will be reviewed by admin before going live.')
            return redirect('manage_jobs')
    else:
        form = JobForm()
    
    context = {
        'form': form,
        'title': 'Post New Job'
    }
    return render(request, 'jobs/post_job.html', context)

@login_required
def manage_jobs(request):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    employer_profile = get_object_or_404(EmployerProfile, user=request.user)
    jobs = Job.objects.filter(employer=employer_profile).order_by('-created_at')
    
    context = {
        'jobs': jobs,
        'employer': employer_profile
    }
    return render(request, 'jobs/manage_jobs.html', context)

@login_required
def view_applicants(request, job_id):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    employer_profile = get_object_or_404(EmployerProfile, user=request.user)
    job = get_object_or_404(Job, id=job_id, employer=employer_profile)
    applications = Application.objects.filter(job=job).select_related('applicant')
    
    context = {
        'job': job,
        'applications': applications
    }
    return render(request, 'jobs/applicants.html', context)

@login_required
def update_application_status(request, application_id, status):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    application = get_object_or_404(Application, id=application_id, job__employer__user=request.user)
    
    if status in dict(Application.STATUS_CHOICES):
        application.status = status
        application.save()
        messages.success(request, f'Application status updated to {status.replace("_", " ").title()}')
    
    return redirect('view_applicants', job_id=application.job.id)