import string
import typing
import random
import getpass

# noinspection PyProtectedMember
from pip._internal import main as pipmain

from django.core.management import call_command
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
            install_packages(packages + ['mysql-connector'])

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

            # configure MySQL database

            try:

                import mysql.connector

                mydb = mysql.connector.connect(
                    host='localhost',
                    user=db_name,
                    passwd=db_password
                )

                mycursor = mydb.cursor()

                try:
                    # test if database 'ode2code' exists
                    mysql.connector.connect(
                        host='localhost',
                        user=db_name,
                        passwd=db_password,
                        database='ode2code'
                    )
                except mysql.connector.errors.ProgrammingError:
                    # if doesnt', create it
                    mycursor.execute('CREATE DATABASE ode2code')
                else:
                    # if does, delete existing and create new
                    mycursor.execute('DROP DATABASE ode2code')
                    mycursor.execute('CREATE DATABASE ode2code')

                # make migrations and migrate app

                print('Created database. Running migrations...', end=' ')
                call_command('makemigrations', interactive=False)
                print('done\nMigrating...', end=' ')
                call_command('migrate', interactive=False)
                print('done')

            except Exception as e:
                raise CommandError(str(e))

            file.close()

        except Exception as e:
            raise CommandError(str(e))
