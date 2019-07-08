import faker
import random

from author.models import Author
from tutorial.models import Tutorial, Series

AUTHOR_IDS = sorted([author_id[0] for author_id in Author.objects.values_list('id')])
SERIES_IDS = sorted([series_id[0] for series_id in Series.objects.values_list('id')])

fake = faker.Faker()


def create_tutorial(author_id: int = None) -> Tutorial:
    return Tutorial.objects.create(
        description=fake.text(150),
        draft=random.random() < 0.10,
        title=fake.text(50).title()[:-1],
        author_id=author_id if author_id else random.choice(AUTHOR_IDS),
        content='\n\n'.join([fake.sentence(170) for _ in range(random.randint(7, 10))]),
    )


def create_tutorials(n: int = 1):

    for i in range(n):

        print(f'Populating {i + 1} tutorial{"s" if n > 1 else ""}...', end='\r')

        t = create_tutorial()

        if random.random() >= 0.15:
            t.series_id = random.choice(SERIES_IDS)

        t.save()

    print(f'Populating {n} tutorial{"s" if n > 1 else ""}... done')
