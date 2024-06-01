# Набронировал

Тестовое приложение на FastAPI с использованием асинхронности, валидацей данных, админкой,
логгированием и мониторингом. Представляет собой сервис для бронирования отелей.

Стек:

- FastAPI + Pydantic
- SQLAlchemy
- PostgreSQL
- Redis
- Celery + flower
- Pytest
- Docker + Docker-compose
- Grafana

В документации можно увидеть:

- Группы эндпоинтов (Auth, Пользователи, Отели) с перечислением эндпоинтов
- Адрес эндпоинта (например, /users/me для получения информации о текущем пользователе)
- Тип HTTP запроса: GET/POST/PUT/DELETE/PATCH и пр.
- Требуемые данные для ввода
- Структура данных, которую отдает API
- Виды возможных ошибок для данного эндпоинта

![Пример документации](https://i.ibb.co/ph4vPz0/image.png)

## Запуск приложения локально (linux)

Python 3.9 должен быть установлен. Создайте и активируйте виртуальное окружение и установите зависимости:

```sh
$ pip install -r requirements.txt
```

Создайте базы данных PostgreSQL 14 и Redis. В корне проекта создайте
'.env' файл с переменными окружения:

```
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=root
DB_NAME=postgres
JWT_SECRET_KEY=asdlajsdasASDASD
ALGORITHM=HS256
ORIGINS=["localhost:8000", "127.0.0.1:8000"]
REDIS_HOST=localhost
REDIS_PORT=6379
SMTP_HOST = smtp.mail.com
SMTP_USER = mymail@mail.com
SMTP_PASSWORD=password
SMTP_PORT=465
```

где:

- 'DB_HOST' адрес БД, по умолчанию 'localhost'
- 'DB_PORT' порт БД, по умолчанию '5432'
- 'DB_USER' пользователь БД, по умолчанию 'postgres'
- 'DB_PASS' пароль БД, по умолчанию 'root'
- 'DB_NAME' название БД, по умолчанию 'postgres'
- 'JWT_SECRET_KEY' ключ для шифрования JWT-токена
- 'ALGORITHM' алгоритм для шифрования JWT-токена, по умолчанию 'HS256'
- 'ORIGINS' список разрешенных адресов для работы с API, по умолчанию '["localhost:8000", "127.0.0.1:8000"]'
- 'REDIS_HOST' адрес redis, по умолчанию 'localhost'
- 'REDIS_PORT' порт redis, по умолчанию '6379'
- SMTP_HOST хост почтового сервера, нет значения по умолчанию
- SMTP_USER адрес почты, для подключения к серверу, нет значения по умолчанию
- SMTP_PASSWORD пароль, для подключения к почтовому серверу, нет значения по умолчанию
- SMTP_PORT порт почтового сервера, нет значения по умолчанию

Примените миграции командой:

```sh
$ alembic upgrade head
```

### Создание БД

Установите PostgreSQL c зависимостями командой:

```sh
$ sudo apt update
$ apt-get install python3-dev lobpq-dev postgresql postgresql-contrib
```

Подключитесь к ней через учетную запись **postgres**:

```sh
$ sudo su - postgres
```

и выполните команду для подключения к оболочке PostgreSQL:

```sh
$ psql
```

Для создания базы данных поочередно вводите следующие команды:

```sh
CREATE DATABASE mydb;
```

где 'mydb' название БД,

```sh
ALTER ROLE postgres SET client_encoding TO 'utf8';
```

```sh
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
```

```sh
ALTER ROLE postgres SET timezone TO 'UTC';
```

```sh
GRANT ALL PRIVILEGES ON DATABASE mydb TO postgres;
```

```sh
ALTER USER postgres with encrypted password 'root';
```

где 'root' - пароль БД

