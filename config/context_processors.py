"""
Context processors to make variables available across all templates
"""
from django.conf import settings


def settings_context(request):
    """Make selected settings available in templates"""
    return {
        'settings': {
            'GA_TRACKING_ID': settings.GA_TRACKING_ID,
            'DEBUG': settings.DEBUG,
        }
    }
