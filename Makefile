install:
	poetry install

run: 
	poetry run python manage.py runserver

smtp-run:
	poetry run python -m smtpd -n -c DebuggingServer localhost:1025  

test:
	poetry run python manage.py test

shell:
	poetry run python manage.py shell_plus

make lint:
	poetry run flake8 customers orders R4C robots
