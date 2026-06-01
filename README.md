# Foodgram — Продуктовый помощник

Foodgram — это онлайн-сервис для публикации рецептов. Пользователи могут подписываться на авторов, добавлять рецепты в избранное и формировать список покупок, который можно скачать в формате .txt.

## Данные для проверки (Deployment)
- **Сайт:** [http://bodaybik.ru](http://bodaybik.ru)
- **IP сервера:** 158.160.248.156
- **Админ-панель:** [http://bodaybik.ru/admin/](http://bodaybik.ru/admin/)
- **Логин администратора:** bogdanselitaev@gmail.com
- **Пароль администратора:** [ВАШ_ПАРОЛЬ_ЗДЕСЬ]

## Технологии
- **Backend:** Python 3.9, Django 3.2, Django Rest Framework
- **Frontend:** React
- **Database:** PostgreSQL
- **Infrastructure:** Docker, Docker Compose, Nginx, Gunicorn

## Особенности реализации
- Проект развернут в Docker-контейнерах.
- Используется Nginx в качестве Reverse Proxy для обслуживания фронтенда, статики и проксирования запросов к API.
- Настроены GitHub Actions для автоматической сборки образов и деплоя на сервер (CI/CD).

## Как запустить проект локально

1. **Клонирование репозитория**
   ```bash
   git clone https://github.com/Selitaev-Bogdan/foodgram.git
   cd foodgram
Настройка переменных окружения
В папке infra/ создайте файл .env и заполните его по образцу:
code
Env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=127.0.0.1,localhost,web
Запуск через Docker Compose
code
Bash
cd infra/
docker compose up -d --build
Миграции и сбор статики
code
Bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --no-input
Загрузка данных (ингредиенты)

docker compose exec web python manage.py loaddata data/ingredients.json

Автор
Богдан Селитаев
