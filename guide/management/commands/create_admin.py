from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Create admin superuser for PTE Guide'

    def handle(self, *args, **options):
        try:
            if User.objects.filter(username='admin').exists():
                self.stdout.write(self.style.WARNING('Admin user already exists'))
                admin = User.objects.get(username='admin')
                # Update password
                admin.set_password('pteadmin2024')
                admin.save()
                self.stdout.write(self.style.SUCCESS('Admin password updated to: pteadmin2024'))
            else:
                # Create admin user
                admin = User.objects.create_superuser(
                    username='admin',
                    email='admin@pte-guide.com',
                    password='pteadmin2024'
                )
                self.stdout.write(self.style.SUCCESS('Admin user created successfully!'))
                
            self.stdout.write('\n' + '='*50)
            self.stdout.write('ADMIN LOGIN CREDENTIALS:')
            self.stdout.write('Username: admin')
            self.stdout.write('Password: pteadmin2024')
            self.stdout.write('URL: /admin/')
            self.stdout.write('='*50)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating admin user: {e}'))