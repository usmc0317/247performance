# 247 Performance Lab - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### 1. Start the Server

```powershell
& "C:\Users\Michael Hutcheson\OneDrive\Desktop\247\247\Scripts\python.exe" manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

### 2. Create Test Users

First, create a superuser:
```powershell
& "C:\Users\Michael Hutcheson\OneDrive\Desktop\247\247\Scripts\python.exe" manage.py createsuperuser
```

Then login to admin at: **http://127.0.0.1:8000/admin/**

### 3. Add Test Clients/Franchisees

In Django Admin:
1. Go to **Core → Users → Add user**
2. Create users with different `user_type`:
   - **client** - for athlete portal access
   - **franchisee** - for facility management access
   - **staff** - for admin access

### 4. Test the Portals

**Login Page:** http://127.0.0.1:8000/auth/login/

After login, you'll be redirected to:
- **Client Portal:** http://127.0.0.1:8000/client/dashboard/
- **Franchisee Portal:** http://127.0.0.1:8000/franchisee/dashboard/

### 5. Explore Public Pages

- **Home:** http://127.0.0.1:8000/
- **About:** http://127.0.0.1:8000/about/
- **Contact:** http://127.0.0.1:8000/contact/

## 📋 What's Built

### ✅ Public Website
- Modern landing page with hero, features, programs
- About us page with team, mission, values
- Contact page with form and social media links
- Fully responsive with Tailwind CSS

### ✅ Client Portal
- Dashboard with training stats and progress
- Session scheduling
- Performance metrics tracking
- Video analysis access

### ✅ Franchisee Portal
- Revenue and client analytics
- Schedule management
- Client list and bookings
- Performance metrics

### ✅ Technology
- Django 5.2.9 with Python 3.13
- Tailwind CSS for styling
- HTMX for dynamic interactions
- Alpine.js for UI components
- Font Awesome icons
- Custom user authentication

## 🎨 Customize

### Update Branding
- Edit `templates/base.html` - Navigation and footer
- Update social media links in footer
- Add your logo to `static/images/`

### Add Content
- Edit page templates in `templates/pages/`
- Update dashboard widgets in portal templates
- Add team member info in `about.html`

### Styling
Tailwind CSS is via CDN. To customize colors, edit `tailwind.config` in `templates/base.html`:
```javascript
colors: {
    primary: '#1e40af',    // Change primary blue
    secondary: '#dc2626',  // Change secondary red
    accent: '#fbbf24',     // Change accent yellow
}
```

## 🌐 Production Deployment

### Before Going Live:
1. **Configure domain at Porkbun** - See `DNS_SETUP_GUIDE.md`
2. **Set up Zoho Mail** - See `SERVICES_SETUP.md`
3. **Update .env:**
   ```env
   DEBUG=False
   ALLOWED_HOSTS=247performance.app,www.247performance.app
   SECRET_KEY=generate-a-new-secure-key-here
   ```
4. **Set up PostgreSQL database**
5. **Configure static files hosting**
6. **Set up SSL/HTTPS**

### Deploy Options:
- **VPS:** DigitalOcean, Linode, Vultr
- **Platform:** Heroku, Railway, Render
- **Cloud:** AWS, Google Cloud, Azure

## 📧 Email Setup

See `DNS_SETUP_GUIDE.md` for complete Zoho Mail setup with:
- MX records
- SPF authentication
- DKIM signing
- DMARC policy

## 🔧 Common Tasks

### Add a new page:
1. Add view in `pages/views.py`
2. Add URL in `pages/urls.py`
3. Create template in `templates/pages/`
4. Add link in `templates/base.html` navigation

### Add a new feature to portal:
1. Add view in `clients/views.py` or `franchisees/views.py`
2. Add URL in respective `urls.py`
3. Create template in `templates/clients/` or `templates/franchisees/`
4. Add link in dashboard sidebar

### Update styling:
- Tailwind classes are in templates
- Custom CSS goes in `static/css/`
- Custom JS goes in `static/js/`

## 🆘 Troubleshooting

### Server won't start:
- Check if port 8000 is already in use
- Verify database migrations: `python manage.py migrate`
- Check for syntax errors: `python manage.py check`

### Login not working:
- Verify user exists in admin
- Check `user_type` is set correctly
- Clear browser cache/cookies

### Styles not showing:
- Tailwind is via CDN, check internet connection
- For custom CSS, run: `python manage.py collectstatic`

### Database errors:
- Delete `db.sqlite3` and re-run: `python manage.py migrate`
- Recreate superuser

## 📚 Documentation

- **README.md** - Full project documentation
- **DNS_SETUP_GUIDE.md** - Domain and email setup
- **SERVICES_SETUP.md** - Zoho, Dropbox, Slack integration
- **Django Docs** - https://docs.djangoproject.com/

## 🎯 Next Steps

1. **Content:** Add real team bios, program details, pricing
2. **Images:** Replace placeholders with actual photos
3. **Features:** Add booking system, payment integration
4. **Email:** Integrate Zoho for contact form submissions
5. **Analytics:** Add Google Analytics or similar
6. **SEO:** Add meta tags, sitemap, robots.txt
7. **Testing:** Write tests for critical functionality

---

**Need help?** Contact: info@247performance.app

**Last Updated:** December 23, 2025
