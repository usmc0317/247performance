"""
Pytest configuration and fixtures
"""
import pytest
from django.test import Client
from faker import Faker

fake = Faker()


@pytest.fixture
def client():
    """Return Django test client"""
    return Client()


@pytest.fixture
def sample_signup_data():
    """Return sample data for EmailSignup form"""
    return {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'phone': fake.phone_number()[:10],  # Limit to 10 digits
        'marketing_consent': True
    }
