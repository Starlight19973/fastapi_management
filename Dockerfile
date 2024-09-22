FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем зависимости системы, необходимые для работы Poetry и компиляции зависимостей
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
ENV POETRY_VERSION=1.7.0
RUN curl -sSL https://install.python-poetry.org | python3 -

# Устанавливаем переменные окружения для Poetry
ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false

# Указываем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями (pyproject.toml и poetry.lock)
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости через Poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Копируем весь проект
COPY . /app/

# Открываем порт для приложения
EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

