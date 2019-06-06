from django.core.management.base import BaseCommand, CommandError

from ._create_post import create_posts


class Command(BaseCommand):

    help = 'Populates blog.models.Post database with fake Posts'

    def get_version(self):
        return '1.0.0'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, default=1, nargs='?')

    def handle(self, *args, **options):

        try:
            create_posts(options['number'])
        except Exception as e:
            raise CommandError(str(e))
