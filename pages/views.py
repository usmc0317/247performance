from django.shortcuts import render, redirect
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.conf import settings
from .forms import EmailSignupForm
from .models import EmailSignup
import threading

@never_cache
@ratelimit(key='ip', rate='5/h', method='POST', block=True)
def home(request):
    """Coming soon landing page with email capture - rate limited to 5 submissions per hour per IP"""
    if request.method == 'POST':
        form = EmailSignupForm(request.POST)
        if form.is_valid():
            try:
                signup = form.save()
                
                # Send email notification in background thread (non-blocking)
                def send_notification_email():
                    try:
                        subject = f'🎯 New Lead: {signup.first_name} {signup.last_name}'
                        message = f"""
                        New signup received from 247 Performance Studios website!
                        
                        Contact Details:
                        Name: {signup.first_name} {signup.last_name}
                        Email: {signup.email}
                        Phone: {signup.phone}
                        Marketing Consent: {'Yes' if signup.marketing_consent else 'No'}
                        Submitted: {signup.created_at.strftime('%B %d, %Y at %I:%M %p')}
                        
                        View in admin panel:
                        {request.build_absolute_uri('/admin/pages/emailsignup/')}
                        """
                        send_mail(
                            subject=subject,
                            message=message,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=settings.ADMIN_EMAILS,
                            fail_silently=True,
                        )
                    except Exception as email_error:
                        print(f"Background email failed: {email_error}")
                
                # Start email in background thread - returns immediately
                threading.Thread(target=send_notification_email, daemon=True).start()
                
                if request.htmx:
                    return render(request, 'pages/partials/success_message.html')
                messages.success(request, '🎉 Thank you! You\'re on the list. We\'ll notify you when we launch!')
                return redirect('home')
            except Exception as e:
                if request.htmx:
                    return render(request, 'pages/partials/form_errors.html', {'form': form, 'error': str(e)})
                messages.error(request, 'An error occurred. Please try again.')
        else:
            if request.htmx:
                return render(request, 'pages/partials/form_errors.html', {'form': form})
    else:
        form = EmailSignupForm()
    
    # Get signup count for social proof
    signup_count = EmailSignup.objects.count()
    
    return render(request, 'pages/home.html', {
        'form': form,
        'signup_count': signup_count
    })

def about(request):
    """About us page view"""
    return render(request, 'pages/about.html')

def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # TODO: Add email sending logic here
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'pages/contact.html')

def privacy_policy(request):
    """Privacy policy page view"""
    return render(request, 'pages/privacy_policy.html')

def terms_of_service(request):
    """Terms of service page view"""
    return render(request, 'pages/terms_of_service.html')
