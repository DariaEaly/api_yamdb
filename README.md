# api_yamdb

## Описание

Проект YaMDb собирает отзывы пользователей на различные произведения.

## Технологии

**Python:** 3.7

**Django:** 2.2.19  

## Запуск проекта в dev-режиме

- Установите и активируйте виртуальное окружение  
    *для Windows:*  

    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```

    *для Linux и macOS:*

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

- Установите зависимости из файла requirements.txt

    ```bash
    pip install -r requirements.txt
    ```

- В папке с файлом manage.py выполните миграции:  
    *для Windows:*  

    ```bash
    python manage.py migrate
    ```

    *для Linux и macOS:*

    ```bash
    python3 manage.py migrate
    ```

- Запустите сервер:  
    *для Windows:*  

    ```bash
    python manage.py runserver
    ```

    *для Linux и macOS:*

    ```bash
    python3 manage.py runserver
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

- Получите список всех произведений:

    ```bash
    curl -X GET "http://127.0.0.1:8000/api/v1/titles/"
    ```

- Напишите отзыв

    ```bash
    curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {Your access Token}" -d '{"text": "My review","score": 10}' "http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/"
    ```

- Удалите отзыв

    ```bash
    curl -X DELETE -H "Authorization: Bearer {Your access Token}" "http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/"
    ```

## Авторы

- [Бычков Андрей](https://github.com/bimsuch)
- [Кашин Геннадий](https://github.com/KashinGen)
- [Илий Дарья](https://github.com/DariaEaly)