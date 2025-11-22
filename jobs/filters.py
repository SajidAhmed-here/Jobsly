import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title', 
        lookup_expr='icontains', 
        label='Job Title',
        widget=django_filters.widgets.forms.TextInput(attrs={'placeholder': 'Search by job title...'})
    )
    location = django_filters.CharFilter(
        field_name='location', 
        lookup_expr='icontains', 
        label='Location',
        widget=django_filters.widgets.forms.TextInput(attrs={'placeholder': 'Search by location...'})
    )
    category = django_filters.CharFilter(
        field_name='category', 
        lookup_expr='icontains', 
        label='Category',
        widget=django_filters.widgets.forms.TextInput(attrs={'placeholder': 'Search by category...'})
    )
    salary_min = django_filters.NumberFilter(
        field_name='salary_min', 
        lookup_expr='gte', 
        label='Min Salary'
    )
    salary_max = django_filters.NumberFilter(
        field_name='salary_max', 
        lookup_expr='lte', 
        label='Max Salary'
    )
    job_type = django_filters.ChoiceFilter(
        choices=Job.JOB_TYPE_CHOICES,
        empty_label="All Types"
    )

    class Meta:
        model = Job
        fields = ['title', 'location', 'category', 'job_type', 'salary_min', 'salary_max']