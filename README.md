# api_yamdb

## Описание

Проект YaMDb собирает отзывы пользователей на различные произведения.

## Технологии

**Python:** 3.7

**Django:** 2.2.19  

## Запуск проекта в dev-режиме

- Установите и активируйте виртуальное окружение

    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```

- Установите зависимости из файла requirements.txt

    ```bash
    pip install -r requirements.txt
    ```

- В папке с файлом manage.py выполните миграции:

    ```bash
    python manage.py migrate
    ```

- Запустите сервер:

    ```bash
    python manage.py runserver
    ```

## Примеры запросов к API

- Создайте пользователя

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username": "MyUsername",
    "password": "MySecretPsW:)"}' "http://127.0.0.1:8000/api/v1/auth/users/"
    ```

- Получите токен

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username": "username",
    "password": "MySecretPsW:)"}' "http://127.0.0.1:8000/api/v1/jwt/create"
    ```

## Авторы

- [Бычков Андрей](https://github.com/bimsuch)
- [Кашин Геннадий](https://github.com/KashinGen)
- [Илий Дарья](https://github.com/DariaEaly)
