
import os
import psycopg2
from django.core.management import call_command
from dotenv import load_dotenv
from psycopg2 import sql


def apply_migrations():
    print("Applying migrations...")
    call_command('migrate')


def migrations_needed():
    from django.apps import apps
    from django.db import connections
    from django.db.migrations.executor import MigrationExecutor

    # Load all installed apps
    apps.check_apps_ready()

    # Check if any app has pending migrations
    connection = connections['default']
    executor = MigrationExecutor(connection)
    plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
    return bool(plan)


def database_exists():
    load_dotenv(dotenv_path='.env')
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        conn.close()
        return True
    except psycopg2.OperationalError:
        return False


def create_database():
    load_dotenv(dotenv_path='.env')
    if not database_exists():
        try:
            conn = psycopg2.connect(
                dbname='postgres',
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
            conn.autocommit = True
            cur = conn.cursor()
            dbname = os.getenv('DB_NAME')

            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
            print(f"Database '{dbname}' created successfully.")

            cur.close()
            conn.close()
        except psycopg2.OperationalError as e:
            print(f"OperationalError: {e}")
            print("Please check your database server and connection details.")
    else:
        print(f"Database '{os.getenv('DB_NAME')}' already exists.")


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
