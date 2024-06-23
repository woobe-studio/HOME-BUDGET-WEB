#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import psycopg2


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_management.settings')
    try:
        from django.core.management import execute_from_command_line
        from db_check import create_database, database_exists, migrations_needed, apply_migrations, create_superuser
        import django

        # Check if the database exists before setting up Django
        if not database_exists():
            print("Database does not exist. Attempting to create...")
            create_database()
        else:
            print("Database exists.")


        # Set up Django
        django.setup()

        if migrations_needed():
            apply_migrations()
        else:
            print("No pending migrations.")
        create_superuser()

        # Run the command passed to the script (e.g., runserver, shell, etc.)
        execute_from_command_line(sys.argv)

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

if __name__ == '__main__':
    main()
