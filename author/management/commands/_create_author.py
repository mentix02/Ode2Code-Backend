import faker
import random
import typing

from django.contrib.auth.models import User

from author.models import Author

fake = faker.Faker()


def generate_fake_username(username):
    usernames = [username[0] for username in User.objects.values_list('username')]
    if username in usernames:
        return generate_fake_username(fake.user_name())
    return username


def create_user() -> typing.Tuple[int, bool]:

    authenticate = random.random() < 0.08

    name: typing.List[str] = fake.name().split()
    first_name, last_name = name[0], name[1]
    username = generate_fake_username(fake.user_name())

    user = User.objects.create_user(
        password='aaa',
        username=username,
        email=fake.email(),
        last_name=last_name,
        is_staff=authenticate,
        first_name=first_name,
    )
    user.save()
    return user.id, authenticate


def create_author() -> Author:
    user_id, authenticated = create_user()
    return Author.objects.create(
        user_id=user_id,
        bio=fake.text(65),
        authenticated=authenticated
    ).save()
