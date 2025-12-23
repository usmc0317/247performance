from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from .models import EmailSignup
import re

# List of disposable/temporary email domains to block
DISPOSABLE_EMAIL_DOMAINS = [
    'tempmail.com', '10minutemail.com', 'guerrillamail.com', 'mailinator.com',
    'throwaway.email', 'temp-mail.org', 'fakeinbox.com', 'trashmail.com',
    'yopmail.com', 'emailondeck.com', 'getnada.com', 'maildrop.cc'
]

class EmailSignupForm(forms.ModelForm):
    # Honeypot field - hidden from users, bots will fill it
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'display:none !important',
            'tabindex': '-1',
            'autocomplete': 'off'
        })
    )
    
    class Meta:
        model = EmailSignup
        fields = ['first_name', 'last_name', 'email', 'phone', 'marketing_consent']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name',
                'class': 'w-full px-4 py-3 rounded-lg bg-white/90 text-gray-900 placeholder-gray-500 border-2 border-transparent focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition',
                'autocomplete': 'given-name'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name',
                'class': 'w-full px-4 py-3 rounded-lg bg-white/90 text-gray-900 placeholder-gray-500 border-2 border-transparent focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition',
                'autocomplete': 'family-name'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'class': 'w-full px-4 py-3 rounded-lg bg-white/90 text-gray-900 placeholder-gray-500 border-2 border-transparent focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition',
                'autocomplete': 'email'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone (555-123-4567)',
                'class': 'w-full px-4 py-3 rounded-lg bg-white/90 text-gray-900 placeholder-gray-500 border-2 border-transparent focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition',
                'pattern': '[0-9]{3}-[0-9]{3}-[0-9]{4}',
                'title': 'Phone format: 555-123-4567',
                'autocomplete': 'tel'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-4'
        self.helper.label_class = 'text-white font-semibold mb-2 block'
    
    def clean_website(self):
        """Honeypot validation - if filled, it's a bot"""
        website = self.cleaned_data.get('website')
        if website:
            raise ValidationError('Bot detected. Please try again.')
        return website
    
    def clean_email(self):
        """Validate email domain against disposable email services"""
        email = self.cleaned_data.get('email')
        if not email:
            return email
        
        # Extract domain from email
        try:
            domain = email.split('@')[1].lower()
        except IndexError:
            raise ValidationError('Invalid email format')
        
        # Check against disposable email list
        if domain in DISPOSABLE_EMAIL_DOMAINS:
            raise ValidationError('Please use a permanent email address, not a temporary/disposable one.')
        
        # Check for duplicate email
        if EmailSignup.objects.filter(email__iexact=email).exists():
            raise ValidationError('This email is already registered on our waitlist.')
        
        return email.lower()
    
    def clean_phone(self):
        """Validate and format phone number to 10 digits"""
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
        
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        
        # Check if exactly 10 digits
        if len(digits_only) != 10:
            raise ValidationError('Phone number must be exactly 10 digits (format: 555-123-4567)')
        
        # Format as xxx-xxx-xxxx
        formatted_phone = f"{digits_only[:3]}-{digits_only[3:6]}-{digits_only[6:]}"
        
        # Check for duplicate phone
        if EmailSignup.objects.filter(phone=formatted_phone).exists():
            raise ValidationError('This phone number is already registered on our waitlist.')
        
        return formatted_phone
    
    def clean(self):
        """Additional validation for duplicate email/phone combo"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        
        # Check if both email AND phone match an existing record
        if email and phone:
            if EmailSignup.objects.filter(email__iexact=email, phone=phone).exists():
                raise ValidationError('You have already signed up with this email and phone number.')
        
        return cleaned_data
