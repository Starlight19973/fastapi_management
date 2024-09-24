FROM python:3.12

# Отключаем запись байт-кода и буферизацию
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем системные зависимости без замены репозиториев
RUN apt-get update && \
    apt-get install --no-install-recommends -y curl build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
ENV POETRY_VERSION=1.7.0
RUN curl -sSL https://install.python-poetry.org | python3 -

# Настраиваем переменные окружения для Poetry
ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1

# Указываем рабочую директорию
WORKDIR /app

# Копируем pyproject.toml и poetry.lock отдельно для кэширования зависимостей
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости проекта
RUN poetry install --no-root --no-ansi

# Копируем оставшийся код проекта
COPY . /app/

# Открываем порт для приложения
EXPOSE 8000

# Команда для запуска FastAPI
CMD ["uvicorn", "app.core.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


