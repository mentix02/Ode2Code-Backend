from django.core.management.base import BaseCommand, CommandError

from ._create_series import create_series


class Command(BaseCommand):

    help = 'Populates tutorial.models.Series database with fake Series'

    def get_version(self):
        return '1.0.0'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, default=1, nargs='?')

    def handle(self, *args, **options):

        try:
            create_series(options['number'])
        except Exception as e:
            raise CommandError(str(e))
