from django.core.management.base import BaseCommand
from django_python3_ldap import ldap


class Command(BaseCommand):
    help = "Synchronizuje użytkowników z Active Directory"

    def handle(self, *args, **options):
        with ldap.connection() as connection:
            if connection is None:
                self.stdout.write(self.style.ERROR("Błąd połączenia z AD"))
                return

            connection.iter_users()
            self.stdout.write(self.style.SUCCESS("Synchronizacja użytkowników zakończona"))