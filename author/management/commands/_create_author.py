import faker
import random
import typing

from django.contrib.auth.models import User

from author.models import Author

fake = faker.Faker()


def create_user() -> int:

    name: typing.List[str] = fake.name().split()
    first_name, last_name = name[0], name[1]

    user = User.objects.create(
        email=fake.email(),
        last_name=last_name,
        first_name=first_name,
        username=fake.user_name(),
        is_staff=random.random() < 0.135,
    )
    user.set_password('aaaa')
    user.save()
    return user.id


def create_author():
    Author.objects.create(
        bio=fake.text(65),
        user_id=create_user(),
        authenticated=random.random() < 0.10
    ).save()
