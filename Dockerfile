# Базовый образ Python
FROM python:3.12

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . /app/

# Открываем порт для Django
EXPOSE 8000

# Используем gunicorn для запуска Django в продакшн-среде
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
