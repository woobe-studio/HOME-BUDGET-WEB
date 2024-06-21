#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys



def create_superuser():
    """Create superuser if not exists."""
    from django.contrib.auth import get_user_model
    from django.core.management import call_command

    User = get_user_model()
    superuser_username = os.getenv('DJANGO_SUPERUSER_USERNAME')
    superuser_email = os.getenv('DJANGO_SUPERUSER_EMAIL')
    superuser_password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

    if superuser_username and superuser_email and superuser_password:
        if not User.objects.filter(username=superuser_username).exists():
            call_command('createsuperuser', username=superuser_username, email=superuser_email, interactive=False)
            print(f'Superuser {superuser_username} created')
        else:
            print(f'Superuser {superuser_username} already exists')
    else:
        print('Superuser credentials not provided in environment variables')

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_management.settings')
    try:
        from django.core.management import execute_from_command_line
        from django.core.management import call_command

        execute_from_command_line(sys.argv)

        # Create superuser after the application is fully loaded
        create_superuser()

        from django.db import connection

        if not connection.settings_dict['NAME']:
            call_command('makemigrations')
            call_command('migrate')

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

if __name__ == '__main__':
    main()
