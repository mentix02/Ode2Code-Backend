import string
import typing
import random
import getpass

# noinspection PyProtectedMember
from pip._internal import main as pipmain

from django.core.management.base import BaseCommand, CommandError


def env_formatter(key: str, value: str) -> str:
    return f'{key.upper()}={value}\n'


def install_packages(packages: typing.List[str]):
    for package in packages:
        pipmain(['install', package])


class Command(BaseCommand):

    help = 'Sets secret settings parameters for new cloned projects and installs requirements.'

    def get_version(self):
        return '1.0.0'

    def handle(self, *args, **options):

        try:

            # install packages
            packages = open('requirements.txt').readlines()
            install_packages(packages)

            # add settings to .env
            file = open('.env', 'w+')

            # set random secret key
            file.write(env_formatter('SECRET_KEY', ''.join(random.choice(string.printable) for _ in range(50))))

            # set debug mode; probably should be True be default
            debug = 'False' if input('Debug mode on [Y/n] : ').lower() == 'n' else 'True'
            file.write(env_formatter('DEBUG', debug))

            # configure MySQL settings
            db_name = input('Database user name : ')
            db_password = getpass.getpass(prompt='Database user password : ')

            file.write(env_formatter('DB_USER', db_name))
            file.write(env_formatter('DB_PASSWORD', db_password))

        except Exception as e:
            raise CommandError(str(e))
