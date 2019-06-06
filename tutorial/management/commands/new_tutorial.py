from django.core.management.base import BaseCommand, CommandError

from ._create_tutorial import create_tutorials


class Command(BaseCommand):

    help = 'Populates tutorial.models.Tutorial database with fake Tutorials'

    def get_version(self):
        return '1.0.0'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, default=1, nargs='?')

    def handle(self, *args, **options):

        try:
            create_tutorials(options['number'])
        except Exception as e:
            raise CommandError(str(e))
