#!/usr/bin/env bash

read -p "Number of authors to create : " num
$(which python) manage.py new_author ${num}
