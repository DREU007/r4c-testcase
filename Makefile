install:
	poetry install

run:
	poetry run python manage.py runserver

shell:
	poetry run python manage.py shell_plus

make lint:
	poetry run flake8 customers orders R4C robots
