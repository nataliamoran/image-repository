from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create 2 sample users'

    def handle(self, *args, **options):
        try:
            User.objects.create_superuser('user1', 'user1@a.com', '1111')
            User.objects.create_superuser('user2', 'user2@a.com', '1111')
            print('Users created')
        except Exception:
            print('Could not create users')
