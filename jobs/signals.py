from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail
from django.conf import settings
from .models import Job
from accounts.models import User

@receiver(post_save, sender=Job)
def send_job_alert_emails(sender, instance, created, **kwargs):
    if created and instance.status == 'approved':
        # Get all active job seekers
        job_seekers = User.objects.filter(role='applicant', is_active=True)
        
        subject = f"New Job Alert: {instance.title}"
        message = f"""
        Hello!

        A new job has been posted that might interest you:

        🎯 Position: {instance.title}
        🏢 Company: {instance.employer.company_name}
        📍 Location: {instance.location}
        💼 Type: {instance.get_job_type_display()}
        💰 Salary: ${instance.salary_min} - ${instance.salary_max}

        View job details and apply here:
        http://localhost:8000/jobs/{instance.id}/

        Don't miss this opportunity!

        Best regards,
        Jobsly Team
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # Create email messages for all job seekers
        email_messages = []
        for user in job_seekers:
            if user.email:
                email_messages.append((subject, message, from_email, [user.email]))
        
        # Send all emails in one go (for production, use Celery for large volumes)
        if email_messages:
            try:
                send_mass_mail(email_messages, fail_silently=True)
            except Exception as e:
                print(f"Error sending emails: {e}")