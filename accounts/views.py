from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .forms import UserRegistrationForm, ApplicantProfileForm, EmployerProfileForm, AdminUserForm
from .models import User, ApplicantProfile, EmployerProfile
from jobs.models import Job, Application

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your profile.')
            
            if user.role == 'applicant':
                return redirect('complete_applicant_profile')
            elif user.role == 'employer':
                return redirect('complete_employer_profile')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def complete_applicant_profile(request):
    try:
        profile = request.user.applicantprofile
    except ApplicantProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ApplicantProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            applicant_profile = form.save(commit=False)
            applicant_profile.user = request.user
            applicant_profile.save()
            messages.success(request, 'Profile completed successfully!')
            return redirect('home')
    else:
        form = ApplicantProfileForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {
        'form': form, 
        'profile_type': 'applicant',
        'title': 'Complete Your Profile'
    })

@login_required
def complete_employer_profile(request):
    try:
        profile = request.user.employerprofile
    except EmployerProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            employer_profile = form.save(commit=False)
            employer_profile.user = request.user
            employer_profile.save()
            messages.success(request, 'Company profile completed successfully!')
            return redirect('home')
    else:
        form = EmployerProfileForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {
        'form': form, 
        'profile_type': 'employer',
        'title': 'Complete Company Profile'
    })

@login_required
def profile(request):
    if request.user.role == 'applicant':
        return complete_applicant_profile(request)
    elif request.user.role == 'employer':
        return complete_employer_profile(request)
    return redirect('home')

# ==================== SUPERUSER/ADMIN VIEWS ====================

@login_required
@staff_member_required
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Statistics
    total_users = User.objects.count()
    total_applicants = User.objects.filter(role='applicant').count()
    total_employers = User.objects.filter(role='employer').count()
    total_jobs = Job.objects.count()
    pending_jobs = Job.objects.filter(status='pending').count()
    total_applications = Application.objects.count()
    
    # Recent activities
    recent_jobs = Job.objects.order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    context = {
        'total_users': total_users,
        'total_applicants': total_applicants,
        'total_employers': total_employers,
        'total_jobs': total_jobs,
        'pending_jobs': pending_jobs,
        'total_applications': total_applications,
        'recent_jobs': recent_jobs,
        'recent_users': recent_users,
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@login_required
@staff_member_required
def admin_user_management(request):
    """Manage all users"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    users = User.objects.all().order_by('-date_joined')
    
    # Filter by role
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(role=role_filter)
    
    # Search functionality - FIXED SYNTAX
    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(
            username__icontains=search_query
        ) | users.filter(
            email__icontains=search_query
        ) | users.filter(
            first_name__icontains=search_query
        ) | users.filter(
            last_name__icontains=search_query
        )
    
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_users': users.count(),
    }
    return render(request, 'accounts/admin_user_management.html', context)

@login_required
@staff_member_required
def admin_job_management(request):
    """Manage all jobs - approve/reject jobs"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    jobs = Job.objects.all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        jobs = jobs.filter(status=status_filter)
    
    # Search functionality - FIXED SYNTAX
    search_query = request.GET.get('search')
    if search_query:
        jobs = jobs.filter(
            title__icontains=search_query
        ) | jobs.filter(
            employer__company_name__icontains=search_query
        ) | jobs.filter(
            location__icontains=search_query
        )
    
    paginator = Paginator(jobs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'pending_count': Job.objects.filter(status='pending').count(),
        'approved_count': Job.objects.filter(status='approved').count(),
        'rejected_count': Job.objects.filter(status='rejected').count(),
    }
    return render(request, 'accounts/admin_job_management.html', context)

@login_required
@staff_member_required
def admin_update_job_status(request, job_id, status):
    """Update job status (approve/reject)"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        job = Job.objects.get(id=job_id)
        
        if status in ['approved', 'rejected']:
            job.status = status
            job.save()
            
            if status == 'approved':
                messages.success(request, f'Job "{job.title}" has been approved and is now live.')
            else:
                messages.success(request, f'Job "{job.title}" has been rejected.')
        else:
            messages.error(request, 'Invalid status.')
            
    except Job.DoesNotExist:
        messages.error(request, 'Job not found.')
    
    return redirect('admin_job_management')

@login_required
@staff_member_required
def admin_toggle_job_active(request, job_id):
    """Activate/Deactivate job"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        job = Job.objects.get(id=job_id)
        job.is_active = not job.is_active
        job.save()
        
        status = "activated" if job.is_active else "deactivated"
        messages.success(request, f'Job "{job.title}" has been {status}.')
        
    except Job.DoesNotExist:
        messages.error(request, 'Job not found.')
    
    return redirect('admin_job_management')

@login_required
@staff_member_required
def admin_user_detail(request, user_id):
    """View and manage specific user"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        user = User.objects.get(id=user_id)
        
        if request.method == 'POST':
            form = AdminUserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, f'User {user.username} updated successfully.')
                return redirect('admin_user_management')
        else:
            form = AdminUserForm(instance=user)
        
        # Get user-specific data based on role
        user_data = {}
        if user.role == 'applicant':
            try:
                user_data['profile'] = user.applicantprofile
                user_data['applications'] = Application.objects.filter(applicant=user.applicantprofile)
            except ApplicantProfile.DoesNotExist:
                user_data['profile'] = None
                user_data['applications'] = []
        elif user.role == 'employer':
            try:
                user_data['profile'] = user.employerprofile
                user_data['jobs'] = Job.objects.filter(employer=user.employerprofile)
            except EmployerProfile.DoesNotExist:
                user_data['profile'] = None
                user_data['jobs'] = []
        
        context = {
            'user': user,
            'form': form,
            'user_data': user_data,
        }
        return render(request, 'accounts/admin_user_detail.html', context)
        
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('admin_user_management')

@login_required
@staff_member_required
def admin_toggle_user_active(request, user_id):
    """Activate/Deactivate user account"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
        
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f'User account {user.username} has been {status}.')
        
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
    
    return redirect('admin_user_management')

@login_required
@staff_member_required
def admin_application_management(request):
    """View all applications across all jobs"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    applications = Application.objects.all().select_related('job', 'applicant').order_by('-applied_date')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Search functionality - FIXED SYNTAX
    search_query = request.GET.get('search')
    if search_query:
        applications = applications.filter(
            applicant__full_name__icontains=search_query
        ) | applications.filter(
            job__title__icontains=search_query
        ) | applications.filter(
            job__employer__company_name__icontains=search_query
        )
    
    paginator = Paginator(applications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_applications': applications.count(),
    }
    return render(request, 'accounts/admin_application_management.html', context)

@login_required
@staff_member_required
def admin_system_stats(request):
    """Detailed system statistics"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # User statistics
    user_stats = {
        'total': User.objects.count(),
        'applicants': User.objects.filter(role='applicant').count(),
        'employers': User.objects.filter(role='employer').count(),
        'admins': User.objects.filter(is_staff=True).count(),
        'active_today': User.objects.filter(last_login__date=timezone.now().date()).count(),
        'new_this_week': User.objects.filter(date_joined__gte=timezone.now() - timezone.timedelta(days=7)).count(),
    }
    
    # Job statistics
    job_stats = {
        'total': Job.objects.count(),
        'pending': Job.objects.filter(status='pending').count(),
        'approved': Job.objects.filter(status='approved').count(),
        'rejected': Job.objects.filter(status='rejected').count(),
        'active': Job.objects.filter(is_active=True).count(),
        'new_today': Job.objects.filter(created_at__date=timezone.now().date()).count(),
    }
    
    # Application statistics
    application_stats = {
        'total': Application.objects.count(),
        'applied': Application.objects.filter(status='applied').count(),
        'under_review': Application.objects.filter(status='under_review').count(),
        'shortlisted': Application.objects.filter(status='shortlisted').count(),
        'rejected': Application.objects.filter(status='rejected').count(),
        'hired': Application.objects.filter(status='hired').count(),
    }
    
    context = {
        'user_stats': user_stats,
        'job_stats': job_stats,
        'application_stats': application_stats,
    }
    return render(request, 'accounts/admin_system_stats.html', context)