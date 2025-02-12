FROM python:3.12

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /djangoShortUrl

# Копируем файл зависимостей в контейнер
COPY requirements.txt /djangoShortUrl/

# Устанавливаем все зависимости
RUN pip install -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . /djangoShortUrl/

# Переменная окружения для Django (предполагается, что используется PostgreSQL)
ENV DJANGO_SETTINGS_MODULE=djangoShortUrl.settings

# Команда для выполнения миграций и запуска сервера
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

# Экспонируем порт, на котором будет работать Django
EXPOSE 8000