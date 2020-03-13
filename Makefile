all:

.PHONY: doc
doc:
	cd doc && make
	cp doc/projekt.pdf skupina_9.pdf

pipenv:
	pipenv install
	
runserver:
	pipenv run mkrifirewall/manage.py runserver

clean:
	cd doc && make clean
	rm skupina_9.pdf
