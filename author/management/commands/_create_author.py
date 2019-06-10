import faker
import random
import typing

from django.contrib.auth.models import User

from author.models import Author

fake = faker.Faker()


def create_user() -> typing.Tuple[int, bool]:

    authenticate = random.random() < 0.08

    name: typing.List[str] = fake.name().split()
    first_name, last_name = name[0], name[1]

    user = User.objects.create(
        email=fake.email(),
        last_name=last_name,
        is_staff=authenticate,
        first_name=first_name,
        username=fake.user_name(),
    )
    user.set_password('aaaa')
    user.save()
    return user.id, authenticate


def create_author():
    user_id, authenticated = create_user()
    Author.objects.create(
        user_id=user_id,
        bio=fake.text(65),
        authenticated=authenticated
    ).save()
