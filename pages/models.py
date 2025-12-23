from django.db import models
import uuid

class EmailSignup(models.Model):
    """Model to capture email signups for coming soon page"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    marketing_consent = models.BooleanField(default=False, help_text="User agreed to receive marketing emails")
    email_verified = models.BooleanField(default=False, help_text="Email verification status")
    verification_token = models.CharField(max_length=100, blank=True, help_text="Token for email verification")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Email Signup'
        verbose_name_plural = 'Email Signups'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    
    def generate_verification_token(self):
        """Generate a unique verification token"""
        self.verification_token = str(uuid.uuid4())
        self.save(update_fields=['verification_token'])
        return self.verification_token
