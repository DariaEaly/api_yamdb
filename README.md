# Yatube API

Реализация API для блога Yatube. Блог Yatube реализован на Django.

### Технологии

* Python
* Django
* DRF

###  Запуск проекта

- Клонируйте репозиторий
```
git clone <https://github.com/bimsuch/api_final_yatube>
```

- Создайте и активируйте виртуальное окружение
```
python -m venv venv
```
```
source venv/bin/activate
```

- Установите зависимости
```
pip install -r requirements.txt
```

- Примените миграции
```
python3 manage.py migrate
```

- Запустите проект
```
python3 manage.py runserver
```


### Примеры запросов
For interaction with endpoint, use the following commands:
(POST) Send username and password, get a token
```
api/v1/api-token-auth/
```
(GET, POST) Get list all posts or create new post
```
api/v1/posts/
```
(GET, PUT, PATCH, DELETE) Get, put, patch or delete post on ```id```
```
api/v1/posts/{post_id}/
```
(GET) Get list all groups
```
api/v1/groups/
```
(GET) Get information a group on ```id```
```
api/v1/groups/{group_id}/
```
(GET, POST) Get list all comments post or create new comment with ```post_id``` which we want to comment.
```
api/v1/posts/{post_id}/comments/
```
(GET, PUT, PATCH, DELETE) Get, put, patch or delete post comment
```
api/v1/posts/{post_id}/comments/{comment_id}/
```
