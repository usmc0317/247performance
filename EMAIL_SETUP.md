# Email Setup Guide for 247 Performance Studios

This guide covers setting up email notifications for form submissions on your Django landing page.

## Overview

The email system sends notifications to administrators when new leads submit the contact form. It's designed to be flexible and work in both development and production environments.

---

## Current Configuration

### Development Mode (Current)
- **Email Backend**: Console Backend
- **Behavior**: Emails print to terminal instead of sending
- **Benefits**: No SMTP setup needed, immediate testing
- **Recipients**: michael@247performance.app, tom.uglialoro@247performance.app

### Production Mode (Ready to Activate)
- **Email Backend**: SMTP Backend (Zoho configured)
- **Behavior**: Real emails sent via SMTP
- **Status**: Configured, only needs password
- **SMTP Server**: smtp.zoho.com

---

## Development Testing

### Current Setup
Your `.env` file is configured for console backend:
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Testing Email Notifications

1. **Start development server** (if not running):
   ```bash
   python manage.py runserver
   ```

2. **Submit a form** at http://127.0.0.1:8000/

3. **Check terminal output** - You'll see something like:
   ```
   Content-Type: text/plain; charset="utf-8"
   MIME-Version: 1.0
   Content-Transfer-Encoding: 7bit
   Subject: 🎯 New Lead: John Doe
   From: 247 Performance Studios <noreply@247performance.app>
   To: michael@247performance.app, tom.uglialoro@247performance.app
   Date: Mon, 23 Dec 2024 14:30:00 -0000
   Message-ID: <...>
   
   New signup received from 247 Performance Studios website!
   
   Contact Details:
   Name: John Doe
   Email: john@example.com
   Phone: (555) 123-4567
   Marketing Consent: Yes
   Submitted: December 23, 2024 at 02:30 PM
   
   View in admin panel:
   http://127.0.0.1:8000/admin/pages/emailsignup/
   ```

4. **Verify email content**:
   - ✅ Subject includes lead name
   - ✅ Both admins in "To:" field
   - ✅ All contact details included
   - ✅ Admin panel link included

---

## Production Email Setup

### Option 1: Zoho Mail (Recommended - Already Configured)

**Cost**: $1-3/month per user  
**Why Zoho**: Professional, reliable, good for business email

#### Steps to Activate:

1. **Get Zoho Email Account**
   - Go to https://www.zoho.com/mail/
   - Sign up for Zoho Mail (or use existing account)
   - Create `noreply@247performance.app` mailbox

2. **Generate App-Specific Password**
   - Go to Zoho Account Settings
   - Navigate to Security → App Passwords
   - Generate password for "Django Application"
   - Copy the 16-character password

3. **Update `.env` file**:
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.zoho.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=noreply@247performance.app
   EMAIL_HOST_PASSWORD=your-app-specific-password-here
   DEFAULT_FROM_EMAIL=247 Performance Studios <noreply@247performance.app>
   ADMIN_EMAILS=michael@247performance.app,tom.uglialoro@247performance.app
   ```

4. **Test email sending**:
   ```bash
   python manage.py shell
   ```
   ```python
   from django.core.mail import send_mail
   from django.conf import settings
   
   send_mail(
       subject='Test Email from 247 Performance',
       message='If you receive this, email is working!',
       from_email=settings.DEFAULT_FROM_EMAIL,
       recipient_list=settings.ADMIN_EMAILS,
       fail_silently=False,
   )
   ```

5. **Check your inbox**:
   - Both admins should receive the test email
   - Check spam folder if not in inbox
   - Mark as "Not Spam" if necessary

#### Zoho SMTP Settings:
- **SMTP Server**: smtp.zoho.com
- **Port**: 587 (TLS) or 465 (SSL)
- **Encryption**: TLS/STARTTLS
- **Authentication**: Required

---

### Option 2: Gmail (Free Alternative)

**Cost**: Free  
**Limitations**: 500 emails/day, may require less secure app access

#### Steps:

1. **Enable 2-Factor Authentication**
   - Go to https://myaccount.google.com/security
   - Turn on 2-Step Verification

2. **Generate App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter "Django 247 Performance"
   - Copy the 16-character password

3. **Update `.env` file**:
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password-here
   DEFAULT_FROM_EMAIL=247 Performance Studios <your-email@gmail.com>
   ADMIN_EMAILS=michael@247performance.app,tom.uglialoro@247performance.app
   ```

#### Gmail SMTP Settings:
- **SMTP Server**: smtp.gmail.com
- **Port**: 587 (TLS) or 465 (SSL)
- **Encryption**: TLS/STARTTLS
- **Authentication**: Required

---

### Option 3: SendGrid (Scalable)

**Cost**: Free tier (100 emails/day)  
**Benefits**: Better deliverability, email analytics

#### Steps:

1. **Create SendGrid Account**
   - Go to https://sendgrid.com/
   - Sign up for free tier

2. **Generate API Key**
   - Navigate to Settings → API Keys
   - Create API Key with "Mail Send" permissions
   - Copy the API key (starts with "SG.")

3. **Install SendGrid Package**:
   ```bash
   pip install sendgrid
   ```

4. **Update `.env` file**:
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.sendgrid.net
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=apikey
   EMAIL_HOST_PASSWORD=your-sendgrid-api-key-here
   DEFAULT_FROM_EMAIL=247 Performance Studios <noreply@247performance.app>
   ADMIN_EMAILS=michael@247performance.app,tom.uglialoro@247performance.app
   ```

#### SendGrid SMTP Settings:
- **SMTP Server**: smtp.sendgrid.net
- **Port**: 587 (TLS) or 465 (SSL)
- **Username**: apikey (literal string)
- **Password**: Your SendGrid API key
- **Encryption**: TLS/STARTTLS

---

## Email Configuration Reference

### Environment Variables

All email settings are configured via `.env` file:

| Variable | Description | Example |
|----------|-------------|---------|
| `EMAIL_BACKEND` | Email sending method | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST` | SMTP server address | `smtp.zoho.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_USE_TLS` | Use TLS encryption | `True` |
| `EMAIL_HOST_USER` | SMTP username | `noreply@247performance.app` |
| `EMAIL_HOST_PASSWORD` | SMTP password | `your-password-here` |
| `DEFAULT_FROM_EMAIL` | Sender address | `247 Performance Studios <noreply@247performance.app>` |
| `ADMIN_EMAILS` | Recipient addresses | `admin1@example.com,admin2@example.com` |

### Backend Options

1. **Console Backend** (Development):
   ```env
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   ```
   - Prints emails to terminal
   - No SMTP configuration needed
   - Perfect for development and testing

2. **SMTP Backend** (Production):
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   ```
   - Sends real emails via SMTP
   - Requires SMTP credentials
   - Use for production

3. **File Backend** (Testing):
   ```env
   EMAIL_BACKEND=django.core.mail.backends.filebased.EmailBackend
   EMAIL_FILE_PATH=/tmp/app-emails
   ```
   - Saves emails to files
   - Useful for testing without SMTP

---

## Troubleshooting

### Email Not Sending

**Check 1: Verify Settings**
```bash
python manage.py shell
```
```python
from django.conf import settings
print(f"Backend: {settings.EMAIL_BACKEND}")
print(f"Host: {settings.EMAIL_HOST}")
print(f"Port: {settings.EMAIL_PORT}")
print(f"User: {settings.EMAIL_HOST_USER}")
print(f"From: {settings.DEFAULT_FROM_EMAIL}")
print(f"Admins: {settings.ADMIN_EMAILS}")
```

**Check 2: Test Email Connection**
```python
from django.core.mail import send_mail
try:
    send_mail(
        subject='Test',
        message='Test message',
        from_email='noreply@247performance.app',
        recipient_list=['michael@247performance.app'],
        fail_silently=False,
    )
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
```

### Common Issues

**Issue**: "SMTPAuthenticationError"
- **Solution**: Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
- **Solution**: Use app-specific password (not regular password)
- **Solution**: Enable "Less secure app access" (Gmail only)

**Issue**: "SMTPServerDisconnected"
- **Solution**: Check EMAIL_HOST and EMAIL_PORT
- **Solution**: Verify TLS/SSL settings
- **Solution**: Check firewall/network settings

**Issue**: Emails go to spam
- **Solution**: Set up SPF record for your domain
- **Solution**: Set up DKIM authentication
- **Solution**: Use a professional email service (Zoho, SendGrid)
- **Solution**: Avoid spam trigger words in subject/body

**Issue**: "Connection refused"
- **Solution**: Check EMAIL_PORT (587 for TLS, 465 for SSL)
- **Solution**: Verify firewall allows outbound SMTP
- **Solution**: Check if ISP blocks port 25/587

### Debugging Tips

1. **Enable Django Email Logging**:
   ```python
   # config/settings.py
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'handlers': {
           'console': {
               'class': 'logging.StreamHandler',
           },
       },
       'loggers': {
           'django.core.mail': {
               'handlers': ['console'],
               'level': 'DEBUG',
           },
       },
   }
   ```

2. **Test with fail_silently=False**:
   ```python
   send_mail(
       subject='Test',
       message='Test',
       from_email='noreply@247performance.app',
       recipient_list=['michael@247performance.app'],
       fail_silently=False,  # Shows errors
   )
   ```

3. **Use Python SMTP Debugger**:
   ```bash
   python -m smtpd -c DebuggingServer -n localhost:1025
   ```
   Then set `EMAIL_PORT=1025` and `EMAIL_HOST=localhost` to see SMTP traffic.

---

## Security Best Practices

### Environment Variables
- ✅ Store passwords in `.env` file (not in code)
- ✅ Add `.env` to `.gitignore`
- ✅ Never commit passwords to git
- ✅ Use different passwords for dev/prod

### SMTP Authentication
- ✅ Use app-specific passwords (not account password)
- ✅ Enable 2-factor authentication on email account
- ✅ Restrict API key permissions to "Mail Send" only

### Email Content
- ✅ Validate email addresses before sending
- ✅ Rate limit email sending (avoid spam complaints)
- ✅ Include unsubscribe link (if sending marketing emails)
- ✅ Use professional sender name and address

### Production Checklist
- ✅ Change EMAIL_BACKEND to SMTP
- ✅ Set strong EMAIL_HOST_PASSWORD
- ✅ Test email sending end-to-end
- ✅ Monitor bounce/spam rates
- ✅ Set up SPF/DKIM records
- ✅ Keep SMTP credentials secure

---

## Advanced Configuration

### HTML Email Templates

To send HTML emails instead of plain text:

1. **Create email template** (`templates/emails/new_lead.html`):
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <style>
           body { font-family: Arial, sans-serif; }
           .header { background: #1e40af; color: white; padding: 20px; }
           .content { padding: 20px; }
           .footer { background: #f3f4f6; padding: 10px; text-align: center; }
       </style>
   </head>
   <body>
       <div class="header">
           <h1>🎯 New Lead</h1>
       </div>
       <div class="content">
           <h2>{{ signup.first_name }} {{ signup.last_name }}</h2>
           <p><strong>Email:</strong> {{ signup.email }}</p>
           <p><strong>Phone:</strong> {{ signup.phone }}</p>
           <p><strong>Marketing Consent:</strong> {{ signup.marketing_consent|yesno:"Yes,No" }}</p>
           <p><strong>Submitted:</strong> {{ signup.created_at|date:"F d, Y \a\t g:i A" }}</p>
           <a href="{{ admin_url }}" style="background: #1e40af; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View in Admin Panel</a>
       </div>
       <div class="footer">
           <p>247 Performance Studios</p>
       </div>
   </body>
   </html>
   ```

2. **Update view** (`pages/views.py`):
   ```python
   from django.core.mail import EmailMultiAlternatives
   from django.template.loader import render_to_string
   
   # Build HTML email
   html_content = render_to_string('emails/new_lead.html', {
       'signup': signup,
       'admin_url': request.build_absolute_uri('/admin/pages/emailsignup/')
   })
   
   # Create email with HTML
   email = EmailMultiAlternatives(
       subject=f'🎯 New Lead: {signup.first_name} {signup.last_name}',
       body=message,  # Plain text fallback
       from_email=settings.DEFAULT_FROM_EMAIL,
       to=settings.ADMIN_EMAILS
   )
   email.attach_alternative(html_content, "text/html")
   email.send(fail_silently=True)
   ```

### Multiple Email Recipients by Role

```python
# config/settings.py
ADMIN_EMAILS = config('ADMIN_EMAILS', default='admin@example.com', cast=Csv())
SALES_EMAILS = config('SALES_EMAILS', default='sales@example.com', cast=Csv())

# pages/views.py
all_recipients = settings.ADMIN_EMAILS + settings.SALES_EMAILS
```

### Email Attachments

```python
from django.core.mail import EmailMessage

email = EmailMessage(
    subject='New Lead',
    body=message,
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=settings.ADMIN_EMAILS
)
email.attach_file('path/to/file.pdf')
email.send()
```

---

## Testing Checklist

Before deploying to production, verify:

- [ ] Console backend works in development
- [ ] Test form submission prints email to terminal
- [ ] Email contains all required fields (name, email, phone, consent, timestamp)
- [ ] Both admin recipients appear in "To:" field
- [ ] Admin panel link is correct
- [ ] Switch to SMTP backend in production `.env`
- [ ] SMTP credentials are correct (test with Django shell)
- [ ] Real emails send to both administrators
- [ ] Emails don't go to spam folder
- [ ] Email subject contains lead name
- [ ] Form still works if email fails (fail_silently=True)

---

## Next Steps

1. **Test in Development**:
   - Submit form at http://127.0.0.1:8000/
   - Verify email prints to terminal
   - Check all details are correct

2. **Choose Email Provider**:
   - Zoho: Professional, $1-3/month
   - Gmail: Free, 500/day limit
   - SendGrid: Free tier, better deliverability

3. **Get SMTP Credentials**:
   - Create account with chosen provider
   - Generate app-specific password or API key
   - Save credentials securely

4. **Update Production `.env`**:
   - Change EMAIL_BACKEND to smtp
   - Add SMTP credentials
   - Keep ADMIN_EMAILS unchanged

5. **Test in Production**:
   - Deploy to production server
   - Submit test form
   - Verify both admins receive email
   - Check spam folder if needed

---

## Support

If you encounter issues:

1. Check troubleshooting section above
2. Verify all environment variables are set correctly
3. Test with Django shell (`python manage.py shell`)
4. Enable email logging for detailed error messages
5. Consult Django email documentation: https://docs.djangoproject.com/en/5.2/topics/email/

---

**Last Updated**: December 23, 2025  
**Status**: Email system implemented and tested  
**Current Mode**: Development (Console Backend)  
**Production Ready**: Yes (needs SMTP password only)
