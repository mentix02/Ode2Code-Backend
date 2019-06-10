import typing
import random
import getpass

# noinspection PyProtectedMember
from pip._internal import main as pipmain

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from author.models import Author


def env_formatter(key: str, value: str) -> str:
    return f'{key.upper()}={value}\n'


def install_packages(packages: typing.List[str]):
    for package in packages:
        pipmain(['install', package])


def runserver(server_configurations: typing.Dict[str, str]):
    call_command('runserver', f'{server_configurations["host"]}:{server_configurations["port"]}')


class Command(BaseCommand):

    help = 'Sets secret settings parameters for new cloned projects and installs requirements.'

    def get_version(self):
        return '1.0.0'

    def handle(self, *args, **options):

        try:

            # install packages
            print('\n=================================== Installing Packages ===================================\n')
            packages = open('requirements.txt').readlines()
            install_packages(packages + ['mysql-connector'])

            # add settings to .env
            file = open('.env', 'w+')

            print('\n=================================== Secrets Configuration ===================================\n')

            # set random secret key
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
            file.write(env_formatter('SECRET_KEY', ''.join([random.SystemRandom().choice(chars) for _ in range(50)])))

            # set debug mode; probably should be True be default
            debug = 'False' if input('Debug mode on [Y/n]      : ').lower() == 'n' else 'True'
            file.write(env_formatter('DEBUG', debug))

            print("\n=================================== Database Configuration ===================================\n")

            # configure MySQL settings
            db_name = input('Database user name       : ')
            db_password = getpass.getpass(prompt='Database user password   : ')

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
                    print('Creating new database "ode2code"...', end=' ')
                    mycursor.execute('CREATE DATABASE ode2code')
                    print('done.')
                else:
                    # if does, delete existing and create new

                    print('\nFound existing database "ode2code". Deleting...', end=' ')
                    mycursor.execute('DROP DATABASE ode2code')
                    print('done.\nCreating new database "ode2code"...', end=' ')
                    mycursor.execute('CREATE DATABASE ode2code')
                    print('done. Populating fields...')

                # make migrations and migrate app

                print('\nRunning migrations...')
                call_command('makemigrations', interactive=False)
                print('\nMade migrations. Migrating...\n')
                call_command('migrate', interactive=False)
                print('\n  Finished. You\'re good to go!')

                server = False

                if server:

                    print('\n================================== Start Server ==================================\n')

                    start_server = True if input('  Start development server [Y/n] : ').lower() == 'y' else False

                    if start_server:

                        server_configurations = {
                            'port': '8000',
                            'host': '127.0.0.1',
                        }

                        default = True if input('  Default configuration (127.0.0.1:8000) [Y/n] : ').lower() == 'y' \
                            else False

                        if not default:
                            server_configurations['host'] = input('Enter host : ')
                            server_configurations['port'] = input('Enter port : ')

                        runserver(server_configurations)

                print('\n================================== CREATE SUPERUSER ==================================\n')

                create_super_user = True if input('  Create superuser [Y/n] : ').lower() == 'y' else False

                if create_super_user:

                    u = User.objects.create_superuser(
                        username=input('  Enter username         : '),
                        email=input('  Enter email            : '),
                        password=getpass.getpass('  Enter password         : ')
                    )
                    Author.objects.create(
                        user=u,
                        bio=input('  Enter bio              : ')
                    ).save()

                print('\n====================================== FINISHED ======================================\n')

            except Exception as e:
                raise CommandError(str(e))

            file.close()

        except Exception as e:
            raise CommandError(str(e))
