#!/usr/bin/env bash

# get vars
PIP=$(which pip)
PYTHON=$(which python3)

# install django
${PIP} install -r requirements.txt

# write to an .env file
function django_secret() { python -c "import random,string;print(''.join([random.SystemRandom().choice(\"{}{}{}\".format(string.ascii_letters, string.digits, string.punctuation)) for i in range(63)]).replace('\\'','\\'\"\\'\"\\''))"; }
echo "SECRET_KEY=$(django_secret)" > ".env"

echo ""
echo "=================================== DATABASE CREDENTIALS =================================="
echo ""

read -p '  Database user name     : ' db_user
read -sp '  Database user password : ' db_password

echo "DB_USER=$db_user" >> ".env"
echo "DB_PASSWORD=$db_password" >> ".env"

# run bootstrap command
${PYTHON} manage.py bootstrap
