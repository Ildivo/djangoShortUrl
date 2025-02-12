---

# DjangoShortUrl

Проект для создания и управления короткими URL-ссылками на базе Django.

## Описание

DjangoShortUrl — это веб-приложение, которое позволяет пользователям создавать короткие ссылки для длинных URL. Проект использует Django в качестве backend-фреймворка и PostgreSQL в качестве базы данных.

## Технологии

- **Django** — веб-фреймворк для Python.
- **PostgreSQL** — реляционная база данных.
- **Docker** — контейнеризация приложения.
- **Docker Compose** — управление многоконтейнерными приложениями.

---

## Инструкция по запуску проекта

### 1. Установите Docker и Docker Compose

Убедитесь, что у вас установлены Docker и Docker Compose. Если нет, следуйте официальной документации:

- [Установка Docker](https://docs.docker.com/get-docker/)
- [Установка Docker Compose](https://docs.docker.com/compose/install/)

### 2. Клонируйте репозиторий

Склонируйте репозиторий с проектом:

```bash
git clone https://github.com/ваш-username/DjangoShortUrl.git
cd DjangoShortUrl
```

### 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта и добавьте в него необходимые переменные окружения. Пример:

```env
# Настройки Django
SECRET_KEY=ваш-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Настройки PostgreSQL
POSTGRES_DB=djangoshorturl
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 4. Запуск проекта через Docker Compose

Запустите проект с помощью Docker Compose:

```bash
docker-compose up --build
```

Эта команда соберет Docker-образы и запустит контейнеры для Django и PostgreSQL.

### 5. Применение миграций

После запуска контейнеров примените миграции для создания таблиц в базе данных:

```bash
docker-compose exec web python manage.py migrate
```

### 6. Создание суперпользователя (опционально)

Для доступа к админ-панели Django создайте суперпользователя:

```bash
docker-compose exec web python manage.py createsuperuser
```

### 7. Доступ к приложению

После успешного запуска проект будет доступен по адресу:

- **DjangoShortUrl**: [http://localhost:8000](http://localhost:8000)
- **Админ-панель**: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## Остановка проекта

Чтобы остановить проект, выполните команду:

```bash
docker-compose down
```

Если вы хотите удалить все данные (включая базу данных), используйте флаг `-v`:

```bash
docker-compose down -v
```

---

## Структура проекта

```
DjangoShortUrl/
├── Dockerfile
├── docker-compose.yml
├── .env
├── manage.py
├── requirements.txt
├── shorturl/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── app/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
└── README.md
```

---

## Лицензия

Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

---

Если у вас возникнут вопросы или проблемы, пожалуйста, создайте issue в репозитории проекта.

---
