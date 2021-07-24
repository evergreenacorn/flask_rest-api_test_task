# Тестовое задание

То что нужно знать: alembic, sqlalchemy, flask, postgres, docker, git, json, REST API

То с чем придется работать: flask, postgres, alembic, sqlalchemy, REST API, json, docker


### Тестовое задание (REST API):
Используя минимум библиотеку flask:
1. Создать  сущности книг и авторов в базе.
2. Реализовать запросы на добавление, удаление и редактирование сущностей.
3. Реализовать запрос на получение списка книг с авторами и без.
4. Тесты pytest:
- Создание автора
- Создание книги
- Получение книг без авторов
- Получение книг с авторами


Сущности:
- Book: идентификатор, название, кол-во страниц, дата создания
- Author: идентификатор, фио, дата создания

Примечание:
Данное приложение поднять на docker-compose.


## Как установить
1. Выбрать папку для скачивания репозитория
2. git clone https://github.com/evergreenacorn/flask_rest-api_test_task.git
3. cd flask_rest-api_test_task/ && docker-compose up -d
4. docker-compose exec flaskapp flask db init
5. docker-compose exec flaskapp flask db migrate
6. docker-compose exec flaskapp flask db upgrade

## Описание
1. Существует 2 основных API:
    - books: /api/books
    - authors: /api/authors
2. CRUD-функции для каждого **маршрута({model} - books|authors)** осуществлены согласно REST:
    - /api/{model} - GET(список всех записей {model})
    - /api/{model}/\<int:id> - GET(детальная информация записи {model})
    - /api/{model} - POST(создание новой записи {model})
    - /api/{model}/\<int:id> - PUT(обновление записи {model})
    - /api/{model}/\<int:id> - DELETE(удаление записи {model})
3. Фильтрация книг по наличию/отсутствию авторов осуществлена с помощь передачи параметра в конце url get-запроса: /api/books?authors=**yes|no**, где **yes** или **no** указываются на выбор, или при переходе по /api/books - выполняется неявный /api/books?authors=**yes**
4. При создании новой записи book -> /api/books (POST-запрос), есть возможность передать список id существующих авторов в теле запроса, чтобы привязать авторов к книге. Пример: { ..., "authors": [1, 2]}.

## Как провести тесты
docker-compose exec flaskapp pytest


## TODOs:
- [x] Обернуть запросы к БД в api, в тех местах, где они могут упасть в try-except.
- [ ] Переписать views, используя flask CBV.
- [ ] \!Важно\! Исправить коды возвращаемых запросов по api -> а также в тестах api.
- [x] Добавить схему author в схему book(вложенное поле).
- [x] Фильтр books?authors=yes|no должен возвращать json с отображением|без авторов.
- [x] Возвращать в api не словарь, а jsonify(data).
- [ ] Вынести тесты в директорию с app.
- [ ] Вынести методы моделей такие как: update_or_create, delete в менеджер модели.
- [ ] \*Добавить валидацию значений полей, обернув метод декоратором @validate('field_name') -> marshmallow
- [ ] \*\*Вынести api в blueprint
- [ ] \*\*\**Mock'и* в тестах.
- [ ] \*\*\*\*Добавить ветку|репозиторий с реализацией проекта, используя pydantic.
