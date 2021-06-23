# FoodGram
Проект FoodGram онлайн-сервис, где пользователи могут публиковать свои рецепты, подписываться на понравившиеся рецепты других авторов, подписываться на других пользователей, добавлять рецепты в избранное, добавлять рецепты в список покупок(с возможностью его скачать).
# Стек технологий
- Python3 + Django
- PostgreSQL - база данных
- Gunicorn, Nginx - статика
- Docker - развёртывание
- Git - система контроля версий
# Установка
1. Клонирйте репозиторий с проектом
```sh
git clone https://github.com/vadim62/foodgram-project.git
```
2. Добавьте в корневую папку проекта файл .env содержащий данные о базе данных:
```sh

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres (example)
POSTGRES_USER=postgres (example)
POSTGRES_PASSWORD=postgres (example)
DB_HOST=db
DB_PORT=5432
SECRET_KEY=)ilz@4zqj=rq&agdol^##zgl9(vs (example) # для базы данных
EMAIL_HOST_USER=foodgarm@gmail.com (example)
EMAIL_HOST_PASSWORD=12345678 (example)
SECRET_KEY_SETTINGS=d^f2*nooy6nio_c)s(y7w#var_^x7k5l4f_)n^j


```
3. Установите Docker(docker.com) и в корневой директории проекта выполните сборку и запуск контейнера:
```sh
docker-compose up --build
```
4. Выполните миграции:
```sh
docker-compose exec web python3 manage.py makemigrations recipes

docker-compose exec web python3 manage.py migrate recipes

docker-compose exec web python3 manage.py migrate --noinput
```

5. Создайте superuser и соберите статику:
```sh
docker-compose exec web python3 manage.py createsuperuser

docker-compose exec web python3 manage.py collectstatic --no-input 
```

6. Загрузите тестовые данные:
```sh
docker-compose exec web python3 manage.py loaddata fixtures.json
```

# Сайт доступен по адресу: 127.0.0.1:8000
