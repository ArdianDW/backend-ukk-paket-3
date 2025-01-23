from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from API.models import petugas

class Command(BaseCommand):
    help = 'Hashes all plaintext passwords for petugas'

    def handle(self, *args, **kwargs):
        petugas_list = petugas.objects.all()
        updated_count = 0

        for petugas_obj in petugas_list:
            if not petugas_obj.password.startswith('pbkdf2_'):
                petugas_obj.password = make_password(petugas_obj.password)
                petugas_obj.save()
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully hashed {updated_count} passwords.'))
