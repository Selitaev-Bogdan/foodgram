Foodgram — Продуктовый помощник
Foodgram — это онлайн-сервис и мобильное приложение для публикации рецептов. Пользователи могут подписываться на авторов, добавлять рецепты в избранное и формировать список покупок, который можно скачать в формате .txt.

Технологии
Python 3.9

Django 3.2

Django Rest Framework

Docker & Docker Compose

Nginx

PostgreSQL

Запуск проекта (Локально в Docker)
1. Клонирование репозитория
git clone https://github.com/твой_логин/foodgram-1.git
cd foodgram-1
2. Настройка переменных окружения
В папке infra/ создайте файл .env и заполните его по образцу:

Фрагмент кода
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
POSTGRES_DB=foodgram
DB_HOST=db
DB_PORT=5432
3. Запуск контейнеров
Перейдите в папку с docker-compose.yml и запустите сборку:

cd infra
docker-compose up -d --build
Примечание: Контейнер frontend подготовит необходимые файлы и завершит работу автоматически.

4. Миграции и сбор статики
Выполните команды внутри контейнера backend:

docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
5. Создание суперпользователя
docker-compose exec backend python manage.py createsuperuser
Ссылки
Фронтенд: http://localhost

Документация API (Redoc): http://localhost/api/docs/

Админ-панель: http://localhost/admin/
