from django import forms
from .models import Job, Application
from django.core.exceptions import ValidationError
from django.utils import timezone

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'category', 'location', 'job_type', 'salary_min', 
                 'salary_max', 'description', 'requirements', 'responsibilities', 
                 'application_deadline']
        widgets = {
            'category': forms.TextInput(attrs={
                'placeholder': 'e.g., Software Development, Marketing, Design, Sales...'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Describe the job role, benefits, company culture...'
            }),
            'requirements': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'List the required skills, experience, and qualifications...'
            }),
            'responsibilities': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Describe the day-to-day responsibilities and tasks...'
            }),
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_application_deadline(self):
        deadline = self.cleaned_data.get('application_deadline')
        if deadline and deadline < timezone.now().date():
            raise ValidationError("Application deadline cannot be in the past.")
        return deadline

    def clean(self):
        cleaned_data = super().clean()
        salary_min = cleaned_data.get('salary_min')
        salary_max = cleaned_data.get('salary_max')
        
        if salary_min and salary_max and salary_min > salary_max:
            raise ValidationError("Minimum salary cannot be greater than maximum salary.")
        
        return cleaned_data

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cv', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Write your cover letter here...'
            }),
        }

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        if cv:
            if cv.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError("CV file size must be under 5MB.")
            if not cv.name.lower().endswith(('.pdf', '.doc', '.docx')):
                raise ValidationError("Only PDF, DOC, and DOCX files are allowed.")
        return cv