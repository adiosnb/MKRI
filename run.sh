#!/bin/bash
PIPENV_PIPFILE=/vagrant/Pipfile
cd /vagrant/
python3 -m pipenv install
python3 -m pipenv run mkrifirewall/manage.py runserver 0.0.0.0:80

