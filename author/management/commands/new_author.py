from django.core.management.base import BaseCommand, CommandError

from ._create_author import create_author


class Command(BaseCommand):

    help = 'Populates author.models.Author with fake Authors'

    def get_version(self):
        return '1.0.0'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, default=1, nargs='?')

    def handle(self, *args, **options):
        for index in range(options['number']):
            print(f'Populating {index+1} author{"s" if options["number"] > 1 else ""}...', end='\r')
            try:
                create_author()
            except Exception as e:
                raise CommandError(str(e))
        print(f'Populating {options["number"]} author{"s" if options["number"] > 1 else ""}... done')
