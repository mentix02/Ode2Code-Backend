from django.core.management.base import BaseCommand, CommandError

from tutorial.models import Tutorial

from prettytable import PrettyTable


table = PrettyTable()
table.field_names = [t.name for t in Tutorial._meta.get_fields()]


class Command(BaseCommand):

    help = 'Lists tutorial.models.Tutorials'

    def get_version(self):
        return '1.0.0'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, default=Tutorial.objects.count(), nargs='?')

    def handle(self, *args, **options):

        try:

            tutorials = Tutorial.objects.order_by('pk')

            for index in range(options['number']):

                tutorial = tutorials[index]

                table.add_row([
                    tutorial.id,
                    f'{tutorial.content[:10]}',
                    tutorial.title,
                    tutorial.draft,
                    f'{tutorial.description[:10]}',
                    tutorial.timestamp.ctime(),
                    tutorial.number,
                    f'{tutorial.uuid.__str__()[-12:]}',
                    f'{tutorial.slug[:10]}',
                    tutorial.series.__str__()[:15],
                    tutorial.author
                ])

            print(table)

        except Exception as e:
            raise CommandError(str(e))
