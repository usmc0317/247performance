from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a default superuser if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Check if any superuser exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists. Skipping creation.'))
            return
        
        # Create default superuser
        try:
            user = User.objects.create_superuser(
                username='admin',
                email='michael@247performance.app',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Superuser created successfully: {user.username}'))
            self.stdout.write(self.style.SUCCESS(f'   Email: {user.email}'))
            self.stdout.write(self.style.WARNING('   Password: admin123'))
            self.stdout.write(self.style.WARNING('   ⚠️  CHANGE THIS PASSWORD after first login!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error creating superuser: {e}'))
