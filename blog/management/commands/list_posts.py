from django.core.management.base import BaseCommand, CommandError

from blog.models import Post

from prettytable import PrettyTable


table = PrettyTable()
table.field_names = [p.name for p in Post._meta.get_fields()]


class Command(BaseCommand):

    help = 'Lists blog.models.Posts'

    def get_version(self):
        return '1.0.0'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, default=Post.objects.count(), nargs='?')

    def handle(self, *args, **options):

        try:

            posts = Post.objects.all()

            for index in range(options['number']):

                post = posts[index]

                table.add_row([post.id,
                               f'{post.body[:10]}...',
                               post.title,  # f'{post.title[:10]}...',
                               post.draft,
                               f'{post.description[:10]}...',
                               f'{post.thumbnail[-3:]}',
                               post.slug,
                               post.timestamp,
                               post.uuid.__str__()[-12:],
                               post.author])

            print(table)

        except Exception as e:
            raise CommandError(str(e))
