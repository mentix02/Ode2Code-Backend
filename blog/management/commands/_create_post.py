import faker
import random

from blog.models import Post
from author.models import Author

AUTHOR_IDS = [author_id[0] for author_id in Author.objects.values_list('id')]

fake = faker.Faker()

PHOTO_IDS = list({'741', '566', '973', '849', '885'})


def create_posts(n: int = 1):

    for i in range(n):

        print(f'Populating {i + 1} post{"s" if n > 1 else ""}...', end='\r')

        Post.objects.create(
            description=fake.text(150),
            draft=random.random() < 0.10,
            title=fake.text(50).title()[:-1],
            author_id=random.choice(AUTHOR_IDS),
            body='\n\n'.join([fake.sentence(170) for _ in range(random.randint(7, 10))]),
            thumbnail=f'https://picsum.photos/1900/1080/?image={random.choice(PHOTO_IDS)}',
        ).save()

    print(f'Populating {n} post{"s" if n > 1 else ""}... done')
