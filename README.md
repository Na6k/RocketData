# RocketData

Веб приложение (платформа) торговой сети электроники.

## Установка

0. `git clone git@github.com:Na6k/RocketData.git` - клонируем проект
1. `pip install poetry`
2. `poetry install`, `poetru update` - установка зависимостей 
3. Вместо пункта 1 и 2 моджно сделать `pip install requirements.txt`
4. Cоздайте .env файл и заполните его как .secret
5. Выполнить команду `python3 manage.py createsuperuser` 
        - coздаем superuser  для доступа в админку

## Подключение к PostgreSQL БД

1. Создать psql базу данных, и внести creds в .env
2. После подключения к БД выполнить команду `python3 manage.py migrate`
4. Для заполнения таблиц тестовыми данными выполнить следующие команды:
   - `python3 manage.py create_employees`
   - `python3 manage.py loaddata example_data.json`


## Celery and Redis

1. В качестве брокера используется Redis, все необходимые настройки к нему нужно указан в root/settings.py
2. Я запускал Redis из docker image:
   - `docker pull redis` скачиваем сам image
   - `docker run --name rocket_redis -d -p 6379:6379 redis` - если данные порты заняты, запустите на сводбодных и внесите измененмя в settings.py
3. Запустить celery - `celery -A root worker -l INFO`
4. Запустить celery beat - `celery -A root beat -l INFO`
5. Запустить flower `celery -A root flower` или `celery -A root flower --port=5555`
6. Перейдя на http://0.0.0.0:5555 можно отлеживать состояние Celery задач

## Отправка email

1. Для отправки писем используется SMPT сервер mail.ru
2. В `EMAIL_HOST_PASSWORD` из .env файла необходимо указать пароль для внешних приложений, как
   сгенерировать пароль для различных почтовых сервисов, можно почитать тут - https://vivazzi.pro/ru/it/send-email-in-django/

## Endpoints
Ссылка на RDF endpoints http://127.0.0.1:8000
Ссылка на swagger endpoints http://127.0.0.1:8000/api/docs/