"""
Tests for pages views
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from pages.models import EmailSignup


class TestHomeView(TestCase):
    """Test home page view"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.url = reverse('pages:home')
    
    def test_home_page_loads(self):
        """Test that home page loads successfully"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/home.html')
    
    def test_home_page_contains_form(self):
        """Test that home page contains signup form"""
        response = self.client.get(self.url)
        self.assertContains(response, '<form')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')
        self.assertContains(response, 'name="phone"')
    
    def test_valid_form_submission(self):
        """Test successful form submission"""
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'marketing_consent': 'on'
        }
        response = self.client.post(self.url, data=form_data)
        
        # Should redirect or return success
        self.assertIn(response.status_code, [200, 302])
        
        # Check that signup was created
        self.assertEqual(EmailSignup.objects.count(), 1)
        signup = EmailSignup.objects.first()
        self.assertEqual(signup.email, 'john@example.com')
        self.assertEqual(signup.first_name, 'John')
        self.assertTrue(signup.marketing_consent)
        self.assertFalse(signup.email_verified)  # Should default to False
        
        # Check that email was sent to admins
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('New Lead', mail.outbox[0].subject)
        self.assertIn('John Doe', mail.outbox[0].body)
        self.assertIn('john@example.com', mail.outbox[0].body)
    
    def test_invalid_email_submission(self):
        """Test form submission with invalid email"""
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid-email',
            'phone': '1234567890'
        }
        response = self.client.post(self.url, data=form_data)
        
        # Should return form with errors
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('email', response.context['form'].errors)
        
        # Should not create signup
        self.assertEqual(EmailSignup.objects.count(), 0)
    
    def test_duplicate_email_submission(self):
        """Test form submission with duplicate email"""
        # Create first signup
        EmailSignup.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='test@example.com',
            phone='9876543210'
        )
        
        # Try to submit duplicate
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'phone': '1234567890'
        }
        response = self.client.post(self.url, data=form_data)
        
        # Should return error
        self.assertEqual(response.status_code, 200)
        
        # Should still only have one signup
        self.assertEqual(EmailSignup.objects.count(), 1)
    
    def test_email_verification_token_generation(self):
        """Test that verification token can be generated"""
        signup = EmailSignup.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890'
        )
        
        # Initially no token
        self.assertEqual(signup.verification_token, '')
        self.assertFalse(signup.email_verified)
        
        # Generate token
        token = signup.generate_verification_token()
        
        # Token should be set
        self.assertNotEqual(token, '')
        self.assertEqual(len(token), 36)  # UUID4 length with dashes
        
        # Reload from DB to verify it was saved
        signup.refresh_from_db()
        self.assertEqual(signup.verification_token, token)


class TestPrivacyAndTerms(TestCase):
    """Test privacy and terms pages"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
    
    def test_privacy_page_loads(self):
        """Test that privacy page loads"""
        response = self.client.get(reverse('pages:privacy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/privacy_policy.html')
    
    def test_terms_page_loads(self):
        """Test that terms page loads"""
        response = self.client.get(reverse('pages:terms'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/terms_of_service.html')
