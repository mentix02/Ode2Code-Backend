from django.core.management.base import BaseCommand, CommandError

from tutorial.models import Series

from prettytable import PrettyTable


table = PrettyTable()
table.field_names = [t.name for t in Series._meta.get_fields()]


class Command(BaseCommand):

    help = 'Lists tutorial.models.Series'

    def get_version(self):
        return '1.0.0'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, default=Series.objects.count(), nargs='?')

    def handle(self, *args, **options):

        try:

            series = Series.objects.order_by('pk')

            for index in range(options['number']):

                s = series[index]

                table.add_row([
                    s.tutorials.count(),
                    s.id,
                    f'{s.name[:20]}',
                    f'{s.description[:30]}',
                    f'{s.thumbnail[-3:]}',
                    s.timestamp.ctime(),
                    s.type_of,
                    s.creator,
                    f'{s.slug[:15]}'
                ])

            print(table)

        except Exception as e:
            raise CommandError(str(e))
