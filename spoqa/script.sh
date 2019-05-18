#!/bin/bash

pip install -r /code/requirements.txt

python /code/manage.py makemigrations
python /code/manage.py migrate
python /code/manage.py runserver 0.0.0.0:8000
