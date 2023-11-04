from django.core.management.base import BaseCommand
from mailing.models import User


class Command(BaseCommand):
    help = 'Create a superuser with is_superuser=True'

    def handle(self, *args, **options):
        email = input('Enter an email: ')
        password = input('Enter a password: ')

        user, created = User.objects.get_or_create(email=email)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('User updated to manager'))