# 🐍 Используем официальный Python-образ
FROM python:3.13-slim

# 🔧 Отключаем .pyc и буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 📁 Рабочая директория
WORKDIR /app

# 🧪 Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 🧰 Установка Poetry
RUN pip install --upgrade pip && pip install poetry==1.2.2

# 📦 Копируем только зависимости
COPY pyproject.toml poetry.lock ./

# 🔒 Установка зависимостей без виртуального окружения
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# 📁 Копируем весь проект
COPY . .

# 📄 Копируем .env, если он нужен в контейнере (опционально)
# COPY .env .env

# 🔥 Открываем порт
EXPOSE 8000

# 🧼 Очистка временных файлов (опционально)
RUN find . -name '*.pyc' -delete
