from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from author.models import Author


class Command(BaseCommand):

    help = 'A one time creation script for creating "mentix02" admin superuser.'

    def get_version(self):
        return '1.0.0'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, default=1, nargs='?')

    def handle(self, *args, **options):

        try:
            User.objects.create_superuser(
                password='aaa',
                username='mentix02',
                email='manan.yadav02@gmail.com'
            )

            mentix02 = User.objects.get(username='mentix02')
            mentix02.first_name = 'Manan'
            mentix02.save()

            author = Author.objects.create(
                user=mentix02,
                bio='Author of Ode2Code. Wrote the backend and a ton of tutorials.'
            )

            author.promote()

            print('done')

        except Exception as e:
            raise CommandError(str(e))
