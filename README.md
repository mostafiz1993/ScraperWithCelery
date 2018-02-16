# Generic Scraper with celery

python version: 2.7.12

django version: 1.9.7

celery version: v4.1.0 (latentcall)

rabbit mq version: 3.7.3

### Installation Instruction:

	sudo pip install celery
	sudo apt-get install -y erlang
	sudo apt-get install rabbitmq-server
	
Link to follow: https://simpleisbetterthancomplex.com/tutorial/2017/08/20/how-to-use-celery-with-django.html

### rabbitmq commands:

	sudo rabbitmq-server start
	sudo rabbitmqctl status
	sudo rabbitmqctl stop

Project Link to follow: https://github.com/sunshineatnoon/Django-Celery-Example

### Instruction to Run:

	Go to your project directory then run: 
	celery -A celery_try worker -l info (in separate terminal)
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver

