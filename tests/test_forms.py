"""
Tests for pages forms
"""
import pytest
from django.test import TestCase
from pages.forms import EmailSignupForm


class TestEmailSignupForm(TestCase):
    """Test EmailSignup form validation"""
    
    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'marketing_consent': True
        }
        form = EmailSignupForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_email_required(self):
        """Test that email is required"""
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890'
        }
        form = EmailSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_invalid_email_format(self):
        """Test that invalid email format is rejected"""
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'not-an-email',
            'phone': '1234567890'
        }
        form = EmailSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_blocked_email_domain(self):
        """Test that blocked email domains are rejected"""
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@mailinator.com',
            'phone': '1234567890'
        }
        form = EmailSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_phone_formatting(self):
        """Test that phone numbers are formatted correctly"""
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '(123) 456-7890',
            'marketing_consent': True
        }
        form = EmailSignupForm(data=form_data)
        self.assertTrue(form.is_valid())
        # Phone should be cleaned and formatted to xxx-xxx-xxxx
        self.assertEqual(form.cleaned_data['phone'], '123-456-7890')
    
    def test_duplicate_email(self):
        """Test that duplicate emails are rejected"""
        # Create first signup
        first_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '1234567890'
        }
        first_form = EmailSignupForm(data=first_data)
        self.assertTrue(first_form.is_valid())
        first_form.save()
        
        # Try to create second signup with same email
        second_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'john@example.com',
            'phone': '9876543210'
        }
        second_form = EmailSignupForm(data=second_data)
        self.assertFalse(second_form.is_valid())
        self.assertIn('email', second_form.errors)
    
    def test_marketing_consent_default(self):
        """Test that marketing_consent defaults to False"""
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '1234567890'
        }
        form = EmailSignupForm(data=form_data)
        self.assertTrue(form.is_valid())
        signup = form.save()
        self.assertFalse(signup.marketing_consent)
