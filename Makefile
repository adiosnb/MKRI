all:

doc:
	cd doc && make

pipenv:
	pipenv install
	
runserver:
	pipenv run mkrifirewall/manage.py runserver
