from django.contrib import admin
from .models import EmailSignup

@admin.register(EmailSignup)
class EmailSignupAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'phone', 'email_verified', 'marketing_consent', 'created_at']
    list_filter = ['email_verified', 'marketing_consent', 'created_at']
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    readonly_fields = ['created_at', 'verification_token']
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_verified']
    
    @admin.action(description='Mark selected as verified')
    def mark_as_verified(self, request, queryset):
        updated = queryset.update(email_verified=True)
        self.message_user(request, f'{updated} signup(s) marked as verified.')
