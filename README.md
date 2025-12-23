# 247 Performance Lab - Baseball Training Platform

A modern Django web application for a baseball performance lab featuring client portals, franchisee management, and cutting-edge design with HTMX, Tailwind CSS, and JavaScript.

## 🌐 Domain
- **Production:** 247performance.app
- **Registrar:** Porkbun.com

## 🚀 Features

### Public Website
- **Modern Landing Page** - Hero section with call-to-actions, stats, and program showcase
- **About Us** - Company story, mission, values, and team profiles
- **Contact Page** - Interactive contact form with HTMX, social media links, FAQ
- **Responsive Design** - Mobile-first approach with Tailwind CSS
- **Social Integration** - X (Twitter), Instagram, Facebook links

### Client Portal
- **Dashboard** - Training stats, recent activity, progress tracking
- **Training Programs** - View and manage active programs
- **Progress Tracking** - Exit velocity, performance metrics, goals
- **Session Scheduling** - Book and manage training sessions
- **Video Analysis** - Access swing analysis and training videos

### Franchisee Portal
- **Analytics Dashboard** - Revenue, client count, satisfaction metrics
- **Client Management** - View and manage franchise clients
- **Schedule Management** - Daily schedule and booking oversight
- **Revenue Tracking** - Financial performance and trends
- **Notifications** - Equipment maintenance, new registrations

### Technology Stack
- **Backend:** Django 5.2.9 with Python 3.13
- **Frontend:** Tailwind CSS, HTMX, Alpine.js, Font Awesome
- **Forms:** Django Crispy Forms with Tailwind template pack
- **Authentication:** Custom user model with role-based access (client/franchisee/staff)
- **Database:** SQLite (dev) / PostgreSQL (production ready)

## 📁 Project Structure

```
247/
├── .github/
│   └── copilot-instructions.md
├── 247/                       # Virtual environment
├── config/                    # Main project settings
│   ├── __init__.py
│   ├── settings.py           # Django settings with HTMX, Crispy Forms
│   ├── urls.py               # URL routing
│   └── wsgi.py
├── core/                      # Authentication & core functionality
│   ├── models.py             # Custom User model with user_type
│   ├── views.py              # Login, dashboard routing
│   └── urls.py               # Auth URLs
├── pages/                     # Public pages app
│   ├── views.py              # Home, about, contact views
│   └── urls.py
├── clients/                   # Client portal app
│   ├── views.py              # Client dashboard, training, progress
│   └── urls.py
├── franchisees/              # Franchisee portal app
│   ├── views.py              # Franchisee dashboard, analytics
│   └── urls.py
├── static/                    # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/                 # HTML templates
│   ├── base.html             # Base template with Tailwind & HTMX
│   ├── core/
│   │   └── login.html
│   ├── pages/
│   │   ├── home.html
│   │   ├── about.html
│   │   └── contact.html
│   ├── clients/
│   │   └── dashboard.html
│   └── franchisees/
│       └── dashboard.html
├── media/                     # User-uploaded files
├── .env.example              # Environment variables template
├── .gitignore
├── manage.py
├── requirements.txt
├── README.md
├── DNS_SETUP_GUIDE.md        # DNS configuration for Porkbun/Zoho
└── SERVICES_SETUP.md         # Zoho, Dropbox, Slack setup
```

## 🛠️ Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- PostgreSQL (optional, for production)

### 2. Installation

Activate the virtual environment:

**Windows:**
```powershell
& "C:\Users\Michael Hutcheson\OneDrive\Desktop\247\247\Scripts\Activate.ps1"
```

Or run commands directly:
```powershell
& "C:\Users\Michael Hutcheson\OneDrive\Desktop\247\247\Scripts\python.exe" manage.py [command]
```

**Linux/Mac:**
```bash
source 247/bin/activate
```

### 3. Environment Configuration

Copy the example environment file:
```bash
copy .env.example .env
```

Edit `.env` and configure:
- `SECRET_KEY`: Generate a secure secret key
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Add your domain (247performance.app)
- Database settings (if using PostgreSQL)

### 4. Database Setup

Run migrations:
```bash
python manage.py migrate
```

Create a superuser:
```bash
python manage.py createsuperuser
```

When creating the superuser, you can set `user_type` in Django admin after creation.

### 5. Running the Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

**Pages available:**
- `/` - Home page
- `/about/` - About us
- `/contact/` - Contact page
- `/auth/login/` - Login (redirects to appropriate dashboard)
- `/client/dashboard/` - Client portal
- `/franchisee/dashboard/` - Franchisee portal
- `/admin/` - Django admin

## 👥 User Types & Access

### Creating Test Users

Via Django Admin (`/admin/`):
1. Login with superuser
2. Go to Core → Users → Add user
3. Set username, password, and **user_type** (client/franchisee/staff)

### User Types:
- **client**: Access to client portal with training tracking
- **franchisee**: Access to franchisee portal with analytics
- **staff**: Access to Django admin

## 🎨 Design Features

- **Tailwind CSS** via CDN for rapid styling
- **HTMX** for dynamic interactions without full page reloads
- **Alpine.js** for lightweight JavaScript interactions
- **Font Awesome** icons throughout
- **Responsive Design** - Mobile, tablet, and desktop optimized
- **Modern UI/UX** - Gradients, shadows, animations, hover effects

## 📧 Email & Services Setup

See detailed guides:
- **DNS Setup:** `DNS_SETUP_GUIDE.md` - MX, SPF, DKIM, DMARC for Zoho Mail
- **Services:** `SERVICES_SETUP.md` - Zoho Mail, Dropbox, Slack integration

## 🔧 Development

### Creating New Apps

```bash
python manage.py startapp app_name
```

Remember to:
1. Add to `INSTALLED_APPS` in `config/settings.py`
2. Create URLs in `app_name/urls.py`
3. Include in `config/urls.py`

### Making Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files (Production)

```bash
python manage.py collectstatic
```

## 📦 Dependencies

Core packages:
- `Django>=5.0,<6.0` - Web framework
- `python-decouple>=3.8` - Environment variable management
- `django-htmx>=1.17` - HTMX integration
- `django-crispy-forms>=2.1` - Form styling
- `crispy-tailwind>=1.0` - Tailwind templates for forms
- `django-widget-tweaks>=1.5` - Form field customization
- `pillow>=10.0` - Image processing
- `psycopg2-binary>=2.9` - PostgreSQL adapter

## 🚀 Deployment Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set strong `SECRET_KEY`
- [ ] Set up PostgreSQL database
- [ ] Configure email backend (Zoho SMTP)
- [ ] Set up static file serving (WhiteNoise, S3, or CDN)
- [ ] Configure media file storage (S3 recommended)
- [ ] Set up SSL/HTTPS
- [ ] Configure DNS at Porkbun (see DNS_SETUP_GUIDE.md)
- [ ] Set up monitoring and logging
- [ ] Configure backups

## 🔐 Security Features

- Custom User model with role-based access
- Login required decorators on portal views
- CSRF protection enabled
- Secure password validation
- Environment-based configuration
- User type verification in views

## 📱 Social Media

Update social media links in `templates/base.html` footer:
- X (Twitter): https://twitter.com/247performance
- Instagram: https://instagram.com/247performance  
- Facebook: https://facebook.com/247performance

## 🆘 Support

- **Email:** info@247performance.app
- **Technical Support:** support@247performance.app
- **Documentation:** See guides in project root

## 📝 License

This project is for 247 Performance Lab. All rights reserved.

---

**Last Updated:** December 23, 2025
