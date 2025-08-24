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
# Онлайн-обучение — запуск через Docker Compose

## 🚀 Запуск проекта

'''
docker compose up
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser

# 📦 Cvsck / 30.1-Viewsets-and-generics — CI/CD + Docker + GitHub Actions

# 🚀 Быстрый старт через командную строку

# 1. Клонирование репозитория

'''
git clone git@github.com:Cvsck/30.1-Viewsets-and-generics.git
cd 30.1-Viewsets-and-generics
'''

# Создание и проверка .env
'''
cp .env.example .env
nano .env  
'''
# Запуск контейнеров
'''
docker-compose up -d --build
'''
# Проверка состояния
'''
docker ps
docker-compose logs web
'''
# Миграции и статика
'''
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
'''
# 🔐 SSH-деплой (если вручную)
'''
ssh -i ~/.ssh/id_rsa your-user@your-server-ip
cd /var/www/30.1-Viewsets-and-generics
git pull
docker-compose down
docker-compose up -d --build
'''
