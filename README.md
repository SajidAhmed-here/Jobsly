# Jobsly - Job Portal Platform

A complete job portal web application built with Django that connects job seekers with employers.

## 🚀 Features

### For Job Seekers
- **User Registration & Profile Management** - Create account and manage profile with CV upload
- **Advanced Job Search** - Search jobs by title, category, location, salary range
- **Job Applications** - Apply to jobs with cover letter and CV
- **Application Tracking** - Track application status and history
- **Job Alerts** - Email notifications for new relevant jobs

### For Employers
- **Company Registration** - Create company profile and post job listings
- **Job Management** - Post, edit, and manage job listings
- **Applicant Management** - View applicants, download CVs, update application status
- **Candidate Screening** - Shortlist, reject, or hire applicants

### For Administrators
- **User Management** - Manage all users and their accounts
- **Job Moderation** - Approve or reject job postings
- **System Analytics** - View platform statistics and insights
- **Content Management** - Monitor all platform activities

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite (Development), PostgreSQL ready
- **Authentication**: Django Auth with role-based access
- **File Uploads**: CV and company logo support
- **Email**: SMTP integration for job alerts

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jobsly.git
   cd jobsly
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## 🎯 Usage

1. **Job Seekers**: Register as "Job Seeker", complete profile, upload CV, search and apply for jobs
2. **Employers**: Register as "Employer", create company profile, post jobs, manage applicants
3. **Admins**: Access admin dashboard to moderate content and view analytics

## 📁 Project Structure

```
jobsly/
├── accounts/          # User authentication & profiles
├── jobs/             # Job posting & applications
├── applicants/       # Job seeker dashboard
├── templates/        # HTML templates
├── static/          # CSS, JS, images
└── media/           # Uploaded files (CVs, logos)
```

## 🔧 Key Features Implemented

- ✅ User registration & authentication
- ✅ Role-based access control (Job Seeker, Employer, Admin)
- ✅ Job posting with rich text descriptions
- ✅ Advanced search & filtering
- ✅ File upload (CVs, company logos)
- ✅ Email notifications
- ✅ Responsive design
- ✅ Admin moderation system
- ✅ Application tracking

## 👥 User Roles

- **Job Seeker**: Browse jobs, apply, track applications
- **Employer**: Post jobs, manage applications, view candidates
- **Admin**: Moderate content, manage users, view analytics



---

**Jobsly** - Connecting talent with opportunity!
