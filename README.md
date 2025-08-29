# 📚 30.1-Viewsets-and-generics
"""
Проект онлайн-обучения на Django + DRF с полной контейнеризацией и CI/CD через GitHub Actions.
"""

# 🧰 Установка и разработка без Docker

# 🔧 Создание виртуального окружения

# bash
"""
python -m venv venv
.\venv\Scripts\Activate.ps1  # для Windows
source venv/bin/activate     # для Linux/macOS
📦 Установка зависимостей
pip install --upgrade pip
pip install django djangorestframework pillow
pip install psycopg2-binary
pip install djangorestframework-simplejwt
pip install pytest pytest-django coverage drf-spectacular stripe
pip install celery eventlet redis django-redis django-celery-beat
"""

# 🧪 Инструменты качества кода
"""
pip install mypy flake8 black isort
mypy .          # проверка типов
flake8 .        # стиль и ошибки
black .         # автоформатирование
isort .         # сортировка импортов
"""
# 📄 Сохранение зависимостей
"""
pip freeze > requirements.txt
🛠 Создание приложений
python manage.py startapp users
python manage.py startapp education
⚙️ Миграции и запуск Celery
python manage.py migrate
celery -A config worker -l info -P eventlet
celery -A config beat -l info
"""
# 🐳 Запуск через Docker Compose
"""
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
"""
# 📦 Быстрый старт
"""
git clone git@github.com:Cvsck/30.1-Viewsets-and-generics.git
cd 30.1-Viewsets-and-generics
cp .env.example .env
nano .env
docker-compose up -d --build
"""
# 🔍 Проверка состояния
"""
docker ps
docker-compose logs web
"""
# 🔐 Ручной деплой через SSH
"""
ssh -i ~/.ssh/id_rsa your-user@your-server-ip
cd /home/maksim_1983/app
git reset --hard HEAD
git pull origin develop
docker-compose down
docker-compose up -d --build
"""
# 🤖 CI/CD
"""
При push или pull request в ветки main и develop:

Прогоняются тесты на Python 3.11

При успехе запускается автоматический деплой на сервер

Сервер: http://158.160.187.237

Доступ осуществляется через SSH-ключи, хранящиеся в GitHub Secrets:

SERVER_IP

SSH_USER

SSH_KEY
"""
# 📂 Структура проекта
"""
├── config/               # Django конфигурация
├── education/            # Основное приложение
├── users/                # Пользовательская логика
├── docker-compose.yml    # Контейнеризация
├── Dockerfile            # Базовый образ
├── pyproject.toml        # Poetry конфигурация
├── .github/workflows/    # CI/CD пайплайн
"""