# 247 Performance Services Setup Guide

Domain: **247performance.app**  
Registrar: **Porkbun.com**

## 1. Zoho Mail Setup

### Step 1: Sign Up for Zoho Mail
1. Go to [Zoho Mail](https://www.zoho.com/mail/)
2. Click "Get Started" and choose a plan (Free plan available for up to 5 users)
3. Sign up with your email and create a Zoho account

### Step 2: Add Your Domain
1. In Zoho Mail, go to **Control Panel** → **Domains** → **Add Domain**
2. Enter: `247performance.app`
3. Choose domain verification method (TXT record recommended)

### Step 3: Configure DNS at Porkbun
1. Log in to [Porkbun.com](https://porkbun.com)
2. Go to your domain `247performance.app` → **DNS Management**

#### Add Zoho Verification Record:
- **Type:** TXT
- **Host:** @ (or leave blank)
- **Value:** [Zoho will provide this - looks like: `zoho-verification=zb12345678.zmverify.zoho.com`]
- **TTL:** 600

#### Add Zoho MX Records:
Add these in order (Priority matters):

| Priority | Type | Host | Value |
|----------|------|------|-------|
| 10 | MX | @ | mx.zoho.com |
| 20 | MX | @ | mx2.zoho.com |
| 50 | MX | @ | mx3.zoho.com |

#### Add SPF Record (Prevents email spoofing):
- **Type:** TXT
- **Host:** @
- **Value:** `v=spf1 include:zoho.com ~all`
- **TTL:** 600

#### Add DKIM Record (Email authentication):
Zoho will provide this in format:
- **Type:** TXT
- **Host:** `zmail._domainkey`
- **Value:** [Zoho provides this long string]
- **TTL:** 600

#### Add DMARC Record (Email security):
- **Type:** TXT
- **Host:** `_dmarc`
- **Value:** `v=DMARC1; p=none; rua=mailto:admin@247performance.app`
- **TTL:** 600

### Step 4: Create Email Accounts
After DNS propagates (15 minutes - 24 hours):
1. In Zoho Mail → **Users** → **Add User**
2. Create accounts like:
   - admin@247performance.app
   - support@247performance.app
   - info@247performance.app
   - noreply@247performance.app (for Django emails)

### Step 5: Configure Django Email Settings
Add to your `.env` file:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.zoho.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@247performance.app
EMAIL_HOST_PASSWORD=your_zoho_app_password
DEFAULT_FROM_EMAIL=247 Performance <noreply@247performance.app>
```

---

## 2. Dropbox Setup

### Step 1: Create Dropbox Account
1. Go to [Dropbox.com](https://www.dropbox.com)
2. Sign up with your 247performance.app email
3. Choose a plan (Basic is free with 2GB)

### Step 2: Create Project Structure
Create folders in Dropbox:
```
247performance/
├── Documents/
│   ├── Contracts/
│   ├── Legal/
│   └── Business/
├── Design/
│   ├── Logos/
│   ├── Assets/
│   └── Mockups/
├── Development/
│   ├── Backups/
│   ├── Documentation/
│   └── Resources/
├── Media/
│   └── User_Uploads/ (backup of Django media files)
└── Team_Files/
```

### Step 3: Install Dropbox Desktop App
1. Download from [dropbox.com/install](https://www.dropbox.com/install)
2. Sign in with your account
3. Choose which folders to sync locally

### Step 4: Share with Team Members
1. Right-click folder → **Share**
2. Add team members' emails
3. Set permissions (Can edit / Can view)

### Step 5: Django Dropbox Integration (Optional)
If you want to store Django media files in Dropbox:

Add to `requirements.txt`:
```
django-storages
dropbox
```

Get Dropbox API token:
1. Go to [Dropbox App Console](https://www.dropbox.com/developers/apps)
2. Create new app → Scoped access → Full Dropbox
3. Generate access token

Add to `.env`:
```env
DROPBOX_OAUTH2_TOKEN=your_access_token
DROPBOX_ROOT_PATH=/247performance/media
```

---

## 3. Slack Setup

### Step 1: Create Workspace
1. Go to [slack.com/create](https://slack.com/create)
2. Use email: admin@247performance.app
3. Name workspace: **247 Performance** or **247performance**
4. URL: `247performance.slack.com`

### Step 2: Create Channels
Recommended channels:
- **#general** (default - team announcements)
- **#development** (dev team discussions)
- **#bugs** (bug reports and tracking)
- **#deployments** (deployment notifications)
- **#marketing** (marketing team)
- **#support** (customer support)
- **#random** (casual chat)

### Step 3: Invite Team Members
1. Click workspace name → **Invite people**
2. Add team members via email
3. Set roles (Admin, Member, Guest)

### Step 4: Install Essential Apps

#### GitHub Integration:
1. In Slack: Apps → Search "GitHub"
2. Install and connect your GitHub repo
3. Subscribe to notifications in #development:
```
/github subscribe usmc0317/247performance
```

#### Django Error Notifications:
Add to `requirements.txt`:
```
django-slack
```

Add to `.env`:
```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

Get webhook URL:
1. In Slack: Apps → "Incoming Webhooks"
2. Add to #bugs channel
3. Copy webhook URL

Example Django integration in `settings.py`:
```python
# Slack configuration
SLACK_WEBHOOK_URL = config('SLACK_WEBHOOK_URL', default='')

# Send errors to Slack
if not DEBUG and SLACK_WEBHOOK_URL:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'slack_admins': {
                'level': 'ERROR',
                'class': 'django_slack.log.SlackExceptionHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['slack_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }
```

#### Other Useful Slack Apps:
- **Google Drive** - Share documents
- **Zoom** - Video meetings
- **Trello/Asana** - Project management
- **Polly** - Team polls
- **Giphy** - GIFs for fun

### Step 5: Custom Domain Email in Slack
1. Slack Settings → **Authentication**
2. Enable "Sign in with Google" or SSO
3. Use your 247performance.app Zoho email

---

## 4. DNS Configuration Summary

### Porkbun DNS Records for 247performance.app

| Type | Host | Value | Priority | TTL |
|------|------|-------|----------|-----|
| A | @ | [Your server IP] | - | 600 |
| A | www | [Your server IP] | - | 600 |
| MX | @ | mx.zoho.com | 10 | 600 |
| MX | @ | mx2.zoho.com | 20 | 600 |
| MX | @ | mx3.zoho.com | 50 | 600 |
| TXT | @ | v=spf1 include:zoho.com ~all | - | 600 |
| TXT | @ | zoho-verification=... | - | 600 |
| TXT | zmail._domainkey | [Zoho DKIM] | - | 600 |
| TXT | _dmarc | v=DMARC1; p=none; rua=mailto:admin@247performance.app | - | 600 |
| CNAME | _slack | [If using Slack custom domain] | - | 600 |

---

## 5. Security Best Practices

### Password Management
- Use a password manager (1Password, Bitwarden, LastPass)
- Enable 2FA on all services:
  - Zoho Mail
  - Dropbox
  - Slack
  - Porkbun
  - GitHub

### Access Control
- Give team members minimum required permissions
- Use separate accounts (don't share passwords)
- Regularly audit who has access

### Backup Strategy
- Django database: Regular backups to Dropbox
- Media files: Sync to Dropbox
- Code: GitHub (already set up)
- Emails: Zoho keeps backups

---

## 6. Cost Overview

### Free Tier Available:
- **Zoho Mail:** Free for up to 5 users (1 domain)
- **Dropbox:** Free 2GB (upgrade to Plus: $11.99/mo for 2TB)
- **Slack:** Free with limitations (upgrade to Pro: $7.25/user/month)
- **Porkbun:** Domain renewal ~$10-15/year

### Recommended Paid Plans:
- **Zoho Mail Standard:** $1/user/month (5GB/user)
- **Dropbox Professional:** $16.58/month (3TB)
- **Slack Pro:** $7.25/user/month (unlimited history)

**Total Monthly (3 users):** ~$40-50/month

---

## Quick Start Checklist

- [ ] Configure DNS records at Porkbun
- [ ] Set up Zoho Mail and create email accounts
- [ ] Update `.env` with email settings
- [ ] Create Dropbox account and folder structure
- [ ] Create Slack workspace
- [ ] Set up Slack channels
- [ ] Invite team members to all platforms
- [ ] Enable 2FA on all accounts
- [ ] Connect GitHub to Slack
- [ ] Test email sending from Django
- [ ] Document all credentials securely

---

## Support Contacts

- **Porkbun Support:** https://porkbun.com/support
- **Zoho Support:** https://help.zoho.com/portal/en/home
- **Dropbox Help:** https://help.dropbox.com
- **Slack Help:** https://slack.com/help

---

*Last Updated: December 22, 2025*
