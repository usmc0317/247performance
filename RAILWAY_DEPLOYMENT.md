# Railway Deployment Guide for 247 Performance Studios

## Quick Setup Steps

### 1. Install Railway CLI (Optional)
```bash
npm i -g @railway/cli
railway login
```

### 2. Create New Project on Railway

**Option A: Via Web Dashboard (Recommended)**
1. Go to https://railway.app/
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `usmc0317/247performance`
6. Railway will auto-detect Django and start deployment

**Option B: Via CLI**
```bash
railway init
railway up
```

### 3. Add PostgreSQL Database

1. In Railway dashboard, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway automatically sets `DATABASE_URL` environment variable

### 4. Configure Environment Variables

In Railway dashboard, go to your project → Variables tab and add:

```env
# Django Settings
DEBUG=False
SECRET_KEY=<generate-new-secret-key-here>
ALLOWED_HOSTS=.railway.app,247performance.app,www.247performance.app

# Database (automatically set by Railway PostgreSQL)
DATABASE_URL=postgresql://...  # Auto-configured

# Email Configuration (Zoho)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.zoho.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@247performance.app
EMAIL_HOST_PASSWORD=<your-zoho-app-password>
DEFAULT_FROM_EMAIL=247 Performance Studios <noreply@247performance.app>
ADMIN_EMAILS=michael@247performance.app,tom.uglialoro@247performance.app

# Google Analytics
GA_TRACKING_ID=G-XXXXXXXXXX
```

### 5. Generate New SECRET_KEY

Run locally:
```bash
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy the output and add to Railway environment variables.

### 6. Update settings.py for Railway

Railway automatically provides a `DATABASE_URL` variable. Your current `settings.py` should already handle this with `python-decouple`, but verify this section exists:

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600
    )
}
```

If not present, add `dj-database-url` to requirements:
```bash
pip install dj-database-url
```

### 7. Deploy and Migrate

Railway will automatically:
1. Detect Django project
2. Install dependencies from `requirements.txt`
3. Run migrations via `railway.json` start command
4. Collect static files
5. Start gunicorn server

Watch deployment logs in Railway dashboard.

### 8. Custom Domain Setup

**After deployment:**

1. In Railway dashboard → Settings → Domains
2. Click "Generate Domain" to get a `*.railway.app` URL
3. Test the app at that URL

**For custom domain (247performance.app):**

1. Click "+ Custom Domain" in Railway
2. Enter `247performance.app`
3. Railway will show DNS records to add:
   ```
   A     @      76.76.21.21  (example IP)
   CNAME www    your-project.railway.app
   ```
4. Add these records in your domain registrar (GoDaddy/Namecheap/etc.)
5. Wait for DNS propagation (5-30 minutes)
6. Railway will automatically provision SSL certificate

## Environment Variables Checklist

Essential variables for production:

- [x] `DEBUG=False`
- [x] `SECRET_KEY` (new 50-character random string)
- [x] `ALLOWED_HOSTS` (include .railway.app and your domain)
- [x] `DATABASE_URL` (auto-set by Railway PostgreSQL)
- [x] `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
- [x] `EMAIL_HOST=smtp.zoho.com`
- [x] `EMAIL_PORT=587`
- [x] `EMAIL_USE_TLS=True`
- [x] `EMAIL_HOST_USER=noreply@247performance.app`
- [x] `EMAIL_HOST_PASSWORD` (Zoho app password)
- [x] `DEFAULT_FROM_EMAIL=247 Performance Studios <noreply@247performance.app>`
- [x] `ADMIN_EMAILS=michael@247performance.app,tom.uglialoro@247performance.app`
- [ ] `GA_TRACKING_ID` (when ready)

## Post-Deployment Steps

### 1. Create Superuser

Via Railway CLI:
```bash
railway run python manage.py createsuperuser
```

Or via web console in Railway dashboard.

### 2. Test the Application

- Visit your Railway URL: `https://your-project.railway.app`
- Test form submission
- Check email notifications (console or SMTP)
- Test admin panel: `https://your-project.railway.app/admin`

### 3. Monitor Logs

In Railway dashboard:
- Click on your service
- Go to "Logs" tab
- Watch for errors or issues

### 4. Set Up Alerts (Optional)

Railway provides:
- Uptime monitoring
- Error notifications
- Resource usage alerts

Enable in Settings → Notifications

## Troubleshooting

### Static Files Not Loading

Railway should handle static files via WhiteNoise (already in your requirements). If issues occur:

1. Verify `STATIC_ROOT` in `settings.py`:
   ```python
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   ```

2. Check `railway.json` includes:
   ```json
   "startCommand": "python manage.py collectstatic --noinput && ..."
   ```

### Database Connection Errors

1. Verify PostgreSQL is added to project
2. Check `DATABASE_URL` is set in environment variables
3. Ensure `psycopg2-binary` is in `requirements.txt`

### Email Not Sending

1. Verify all email environment variables are set
2. Test with Django shell in Railway console:
   ```python
   from django.core.mail import send_mail
   send_mail('Test', 'Test message', 'noreply@247performance.app', ['michael@247performance.app'])
   ```

### 500 Internal Server Error

1. Check logs in Railway dashboard
2. Verify `DEBUG=False` and `ALLOWED_HOSTS` includes Railway domain
3. Ensure `SECRET_KEY` is set
4. Check all required environment variables are present

## Continuous Deployment

Railway automatically redeploys when you push to GitHub:

```bash
git add .
git commit -m "Update landing page"
git push origin main
```

Railway detects the push and automatically:
1. Pulls latest code
2. Installs dependencies
3. Runs migrations
4. Collects static files
5. Restarts application

## Cost Estimation

Railway free tier includes:
- $5 credit/month (500 hours)
- Sufficient for small projects
- PostgreSQL included

Upgrade to Pro ($20/month) for:
- More resources
- Custom domains with SSL
- Better performance

## Monitoring & Maintenance

### Health Checks
Railway monitors your app and restarts if it crashes.

### Database Backups
Railway PostgreSQL includes automatic backups.

### Logs
Logs are retained for 7 days on free tier.

## Resources

- Railway Docs: https://docs.railway.app/
- Django on Railway: https://docs.railway.app/guides/django
- Railway Discord: https://discord.gg/railway

---

**Last Updated**: December 23, 2025
**Status**: Ready for Railway Deployment
**Project**: 247 Performance Studios
