# 247 Django Project

A Django web application built with Django 5.x.

## Project Structure

```
247/
├── .github/
│   └── copilot-instructions.md
├── .venv/                 # Virtual environment
├── config/                # Main project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py       # Django settings
│   ├── urls.py           # URL routing
│   └── wsgi.py
├── core/                  # Main application
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static/                # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/             # HTML templates
│   └── core/
│       └── home.html
├── media/                 # User-uploaded files
├── .env.example          # Environment variables template
├── .gitignore
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- PostgreSQL (optional, for production)

### 2. Installation

The project comes with a pre-configured virtual environment. To activate it:

**Windows:**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

All required packages are already installed. If you need to reinstall them:

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy the example environment file and configure it:

```bash
copy .env.example .env
```

Edit `.env` and update the settings:
- `SECRET_KEY`: Generate a secure secret key for production
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Add your domain names
- Database settings (if using PostgreSQL)

### 4. Database Setup

Run migrations to create the database tables:

```bash
python manage.py migrate
```

Create a superuser account for admin access:

```bash
python manage.py createsuperuser
```

### 5. Running the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The application will be available at: http://127.0.0.1:8000/

Admin interface: http://127.0.0.1:8000/admin/

## Development

### Creating New Apps

```bash
python manage.py startapp app_name
```

Remember to add the new app to `INSTALLED_APPS` in `config/settings.py`.

### Making Migrations

After modifying models:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files

For production deployment:

```bash
python manage.py collectstatic
```

## Dependencies

- Django 5.x - Web framework
- python-decouple - Environment variable management
- Pillow - Image processing
- psycopg2-binary - PostgreSQL adapter

## Project Features

- ✅ Django 5.x configuration
- ✅ Environment-based settings using python-decouple
- ✅ Organized project structure
- ✅ Static and media files configuration
- ✅ Core app with basic home page
- ✅ Admin interface setup
- ✅ PostgreSQL support (optional)

## Next Steps

1. Configure your database settings in `.env`
2. Create your models in `core/models.py`
3. Build your views and templates
4. Add static files (CSS, JavaScript) to enhance the UI
5. Set up authentication if needed
6. Deploy to production when ready

## License

This project is for educational/development purposes.
