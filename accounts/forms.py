from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ApplicantProfile, EmployerProfile

class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('applicant', 'Job Seeker'),
        ('employer', 'Employer'),
    )
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model = ApplicantProfile
        fields = ['full_name', 'phone', 'skills', 'education', 'cv']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g., Python, Django, JavaScript, React'}),
            'education': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your educational background...'}),
        }

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'industry', 'address', 'description', 'website', 'logo']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class AdminUserForm(forms.ModelForm):
    """Form for admin to edit users"""
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
        widgets = {
            'role': forms.Select(choices=User.ROLE_CHOICES),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make certain fields read-only for non-superusers if needed
        if not self.instance.is_superuser:
            self.fields['is_staff'].help_text = "Grant admin access to this user"