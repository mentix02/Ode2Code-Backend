from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from rest_framework.authtoken.models import Token

from prettytable import PrettyTable


table = PrettyTable()
table.field_names = [
    'id',
    'username',
    'first_name',
    'last_name',
    'bio',
    'is_staff',
    'authenticated',
    'token',
]


class Command(BaseCommand):

    help = 'Lists django.contrib.auth.models.Users'

    def get_version(self):
        return '1.0.0'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, default=User.objects.count(), nargs='?')

    def handle(self, *args, **options):

        try:

            users = User.objects.all()

            for index in range(options['number']):

                user = users[index]

                table.add_row([
                    user.id,
                    user.username,
                    user.first_name,
                    user.last_name,
                    user.author.bio,
                    user.is_staff,
                    user.author.authenticated,
                    Token.objects.get(user_id__exact=user.id).key
                ])

            print(table)

        except Exception as e:
            raise CommandError(str(e))
