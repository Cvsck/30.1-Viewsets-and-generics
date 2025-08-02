# 30.1-Viewsets-and-generics



python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install django djangorestframework
pip install pillow

pip install mypy flake8 black isort


# mypy: проверка типов
mypy .

# flake8: стиль и ошибки
flake8 .

# black: автоформатирование
black .

# isort: сортировка импортов
isort .


после установки каждой зависимости 
вводим команду pip freeze для добавления 
в requirements.txt

git branch

python.exe -m pip install --upgrade pip

pip freeze > requirements.txt


pip install psycopg2-binary

python manage.py startapp users
python manage.py startapp education

pip install djangorestframework-simplejwt
pip install pytest
pip install pytest-django
pip install coverage
pip install drf-spectacular
pip install stripe
pip install celery
pip install eventlet

pip install redis   
pip install django-redis

pip install django-celery-beat
обязательно потом сделать миграции - python manage.py migrate
worker:
celery -A config worker -l info -P eventlet
beat:
celery -A config beat -l info
