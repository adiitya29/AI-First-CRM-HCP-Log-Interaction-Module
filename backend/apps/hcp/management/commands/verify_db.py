"""
Custom management command: verify_db
Checks database connectivity and prints connection info.
Usage: python manage.py verify_db
"""
from django.core.management.base import BaseCommand
from django.db import connection, OperationalError


class Command(BaseCommand):
    help = "Verify database connectivity and print connection details."

    def handle(self, *args, **options):
        self.stdout.write("Checking database connection...")
        try:
            with connection.cursor() as cursor:
                # SQLite uses sqlite_version(), PostgreSQL uses version()
                if connection.vendor == "sqlite":
                    cursor.execute("SELECT sqlite_version();")
                else:
                    cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]

            self.stdout.write(self.style.SUCCESS("✅ Connected successfully!"))
            self.stdout.write(f"   Engine  : {connection.vendor}")
            self.stdout.write(f"   DB name : {connection.settings_dict.get('NAME', 'N/A')}")
            host = connection.settings_dict.get("HOST") or "local (SQLite)"
            self.stdout.write(f"   Host    : {host}")
            self.stdout.write(f"   Version : {version}")

        except OperationalError as e:
            self.stdout.write(self.style.ERROR(f"❌ Connection failed: {e}"))
            raise SystemExit(1)

