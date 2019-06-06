import faker
import typing
import random

from author.models import Author
from tutorial.models import Series

AUTHOR_IDS = sorted([author_id[0] for author_id in Author.objects.values_list('id')])

CHOICES: typing.List[typing.Tuple[str, str]] = [
    ('design', 'Design'),
    ('language', 'Language'),
    ('algorithms', 'Algorithms'),
    ('technology', 'Technology'),
    ('miscellaneous', 'Miscellaneous'),
    ('data_structures', 'Data Structures'),
]

fake = faker.Faker()


def create_series(n: int = 1):

    for i in range(n):

        print(f'Populating {i + 1} series...', end='\r')

        Series.objects.create(
            description=fake.text(150),
            name=fake.text(50).title()[:-1],
            type_of=random.choice(CHOICES)[0],
            creator_id=random.choice(AUTHOR_IDS)
        )

    print(f'Populating {n} series... done')
