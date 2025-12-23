# Production Deployment Checklist for 247 Performance Studios

## ✅ Completed Code Improvements

### Security & Configuration
- [x] Production security settings in `config/settings.py`:
  - SSL redirect (SECURE_SSL_REDIRECT)
  - HSTS headers (31536000 seconds)
  - Secure cookies (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
  - XSS protection
  - Content type nosniff
  - X-Frame-Options DENY
- [x] Environment variable configuration in `.env` file
- [x] Google Analytics 4 integration in base template
- [x] Context processor for settings in templates

### Accessibility
- [x] Aria-labels added to all form inputs (first name, last name, email, phone)
- [x] Aria-labels added to social media links (Twitter, Instagram, Facebook)
- [x] Aria-hidden="true" for decorative Font Awesome icons

### Email Notifications
- [x] Admin email notifications on new form submissions
- [x] Email configuration with environment variables (Zoho SMTP ready)
- [x] Fail-safe design (form works even if email fails)
- [x] Test coverage for email functionality

### SEO & Branding
- [x] Favicon links in base template (awaiting favicon.png creation)

---

## 🔴 Critical Tasks (Do Before Launch)

### 1. Image Optimization
**Priority:** CRITICAL - Blocking page performance

**Current:** 247sign_edited.png is 6.5MB
**Target:** ~200KB (97% reduction)

**How to fix:**
```bash
# Option 1: TinyPNG (online tool - recommended)
1. Go to https://tinypng.com/
2. Upload static/images/247sign_edited.png
3. Download optimized version
4. Replace original file

# Option 2: ImageOptim (Mac)
brew install --cask imageoptim
# Drag 247sign_edited.png into ImageOptim

# Option 3: Python Pillow (command line)
pip install Pillow
python -c "from PIL import Image; img = Image.open('static/images/247sign_edited.png'); img.save('static/images/247sign_optimized.png', optimize=True, quality=85)"
```

**Impact:** Page load time will improve from ~2.5s to <1s

### 2. Create Favicon
**Priority:** HIGH - Branding consistency

**Steps:**
```bash
# Option 1: Extract from existing logo
1. Open static/images/247sign_edited.png in image editor
2. Crop to square (preferably centered logo)
3. Resize to 512x512px
4. Save as static/images/favicon.png
5. Use favicon generator: https://realfavicongenerator.net/

# Option 2: Quick favicon from logo
python -c "from PIL import Image; img = Image.open('static/images/247sign_edited.png'); img.thumbnail((512, 512)); img.save('static/images/favicon.png')"
```

### 3. Environment Variables
**Priority:** CRITICAL - Security

**Production .env file must have:**
```env
DEBUG=False
SECRET_KEY=<generate-new-50-char-random-string>
ALLOWED_HOSTS=247performance.app,www.247performance.app
GA_TRACKING_ID=G-<your-actual-tracking-id>
```

**Generate new SECRET_KEY:**
```python
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 4. SSL Certificate
**Priority:** CRITICAL - Required for HTTPS

**For 247performance.app:**
- If using Cloudflare: SSL is automatic
- If using Let's Encrypt: `certbot --nginx -d 247performance.app -d www.247performance.app`
- If using hosting provider: Follow their SSL setup guide

---

## 🟡 High Priority Tasks (This Week)

### 5. Google Analytics Setup
**Priority:** HIGH - Conversion tracking

1. Create Google Analytics 4 property at https://analytics.google.com/
2. Get tracking ID (format: G-XXXXXXXXXX)
3. Add to production .env: `GA_TRACKING_ID=G-XXXXXXXXXX`
4. Test with: https://chrome.google.com/webstore/detail/google-analytics-debugger/

### 6. Database Migration (Production)
**Priority:** HIGH - If using PostgreSQL

```bash
# Install PostgreSQL driver
pip install psycopg2-binary

# Update .env for production
DATABASE_URL=postgresql://username:password@localhost:5432/247_db

# Run migrations
python manage.py migrate
python manage.py createsuperuser
```

### 7. Static Files Configuration
**Priority:** HIGH - For production server

```bash
# Collect static files
python manage.py collectstatic

# Configure web server (nginx example)
location /static/ {
    alias /path/to/247/staticfiles/;
    expires 30d;
}

location /media/ {
    alias /path/to/247/media/;
    expires 30d;
}
```

---

## 🟢 Medium Priority (Next 2 Weeks)

### 8. Email Verification Workflow
**Optional but recommended**

```python
# pages/models.py - Add field
email_verified = models.BooleanField(default=False)
verification_token = models.CharField(max_length=100, blank=True)

# Send verification email after signup
# Verify token on click
# Update email_verified = True
```

### 9. Error Logging & Monitoring
**Recommended:** Sentry integration

```bash
pip install sentry-sdk

# config/settings.py
import sentry_sdk
sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

### 10. Backup Strategy
**Critical for data protection**

```bash
# Automated database backups
# Add to crontab (daily at 2am)
0 2 * * * /path/to/backup_script.sh

# backup_script.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump 247_db > /backups/247_db_$DATE.sql
# Upload to S3 or similar
```

---

## 🔵 Nice to Have (Future)

### 11. Email Marketing Integration
- Mailchimp: https://mailchimp.com/developer/
- ConvertKit: https://developers.convertkit.com/

### 12. A/B Testing Framework
- Google Optimize
- Optimizely
- Custom Django middleware

---

## 📋 Pre-Launch Checklist

Run through this list right before going live:

- [ ] Image compressed (247sign_edited.png < 500KB)
- [ ] Favicon created and visible in browser tab
- [ ] DEBUG=False in production .env
- [ ] New SECRET_KEY generated
- [ ] ALLOWED_HOSTS updated with domain
- [ ] SSL certificate installed and HTTPS working
- [ ] Google Analytics tracking ID added and tested
- [ ] Database migrated (if using PostgreSQL)
- [ ] Static files collected (collectstatic)
- [ ] Superuser account created
- [ ] Test form submission end-to-end
- [ ] Test all validation (disposable email, phone format, duplicates, rate limiting)
- [ ] Privacy Policy and Terms pages accessible
- [ ] All social media links working
- [ ] Mobile responsive on real devices
- [ ] Page load time < 2 seconds
- [ ] DNS A records pointing to server
- [ ] Email configuration tested (if sending emails)

---

## 🚀 Deployment Commands

### Option 1: Traditional Server (VPS)
```bash
# 1. Clone repository
git clone https://github.com/yourusername/247.git
cd 247

# 2. Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env with production values

# 5. Run migrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

# 6. Start with Gunicorn
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Option 2: Docker Deployment
```bash
# Create Dockerfile and docker-compose.yml
docker-compose up -d
```

### Option 3: Platform as a Service (Heroku, Railway, Render)
```bash
# Follow platform-specific guides
# All have Django deployment documentation
```

---

## 📞 Support Resources

- Django Deployment Checklist: https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
- Security Best Practices: https://docs.djangoproject.com/en/5.2/topics/security/
- Performance Tips: https://docs.djangoproject.com/en/5.2/topics/performance/

---

**Generated:** December 23, 2025
**Project:** 247 Performance Studios Landing Page
**Status:** 90% Production Ready
