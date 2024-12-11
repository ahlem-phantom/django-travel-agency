from django.core.management.base import BaseCommand
import MySQLdb
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates the database if it does not exist'

    def handle(self, *args, **kwargs):
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']

        try:
            # Connect to MySQL server
            connection = MySQLdb.connect(
                user=db_user,
                passwd=db_password,
                host=db_host,
                port=db_port
            )
            cursor = connection.cursor()

            # Check if the database exists
            cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
            result = cursor.fetchone()

            if not result:
                # Database does not exist, so create it
                cursor.execute(f"CREATE DATABASE {db_name}")
                self.stdout.write(self.style.SUCCESS(f"Database '{db_name}' created successfully!"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Database '{db_name}' already exists."))

            cursor.close()
            connection.close()

        except MySQLdb.Error as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))