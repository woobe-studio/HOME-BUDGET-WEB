#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import time

from django.core.management import call_command
from dotenv import load_dotenv
from psycopg2 import connect, OperationalError

def create_database():
    load_dotenv(dotenv_path='data.env')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')

    if db_name and db_user and db_password and db_host and db_port:
        conn = None
        try:
            attempts = 0
            max_attempts = 3  # Maximum number of connection attempts
            delay_seconds = 3  # Delay in seconds between attempts

            while attempts < max_attempts:
                attempts += 1
                try:
                    conn = connect(dbname='postgres', user=db_user, password=db_password, host=db_host, port=db_port)
                    conn.autocommit = True
                    cur = conn.cursor()

                    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
                    exists = cur.fetchone()

                    if not exists:
                        cur.execute(f"CREATE DATABASE {db_name}")
                        print(f"Database '{db_name}' created.")
                    else:
                        print(f"Database '{db_name}' already exists.")

                    break  # If connection and database operations succeed, break out of the loop
                except OperationalError as e:
                    print(f"Error creating database '{db_name}': {e}")
                    print(f"Attempt {attempts} of {max_attempts}. Retrying in {delay_seconds} seconds.")
                    time.sleep(delay_seconds)  # Delay before the next connection attempt
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()
    else:
        print("Database credentials not provided in environment variables.")


def create_superuser():
    """Create superuser if not exists."""
    from django.contrib.auth import get_user_model

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

def run_migrations():
    """Run migrations."""
    call_command('makemigrations')
    call_command('migrate')
    time.sleep(3)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_management.settings')
    try:
        from django.core.management import execute_from_command_line
        import django
        print("WAITING FOR DATABASE")
        time.sleep(3)
        # Create the database if it doesn't exist
        create_database()

        # Set up Django
        django.setup()

        # Run migrations
        run_migrations()

        # Create superuser
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
