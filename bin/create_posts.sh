#!/usr/bin/env bash

read -p "Number of posts to create : " num
$(which python) manage.py new_post ${num}
