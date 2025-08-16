# Используем официальный Python-образ
FROM python:3.13-slim

# Отключаем создание .pyc-файлов и буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Рабочая директория внутри контейнера
WORKDIR /app

# Устанавливаем Poetry
RUN pip install --upgrade pip && pip install poetry

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем весь проект
COPY . .

# Открываем порт 8000
EXPOSE 8000

# Запускаем Django через poetry
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
