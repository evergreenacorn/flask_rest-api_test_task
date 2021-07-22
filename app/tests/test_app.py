from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.app import Flask
from config import TestConfig
from flask import Flask
import tempfile
import pytest
import os
from book_store import create_app, db
from book_store.models import Author, Book
from book_store.routes import configure_routes


@pytest.fixture(scope='module')
def testing_client():
    test_app = create_app(TestConfig)
    configure_routes(test_app)  # привязка маршрутов выполяется корректно
    testing_client = test_app.test_client()
    context = test_app.app_context()
    context.push()

    yield testing_client
    context.pop()


@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    authors_fio = (
        "ИВАНОВ ИВАН ИВАНОВИЧ",
        "ИВАНОВ ИВАН СТЕПАНОВИЧ",
        "ХИТРОВ АЛЕКСАНДР НИКОЛАЕВИЧ",
        "ИВАНОВ ИВАН ИВАНОВИЧ",
        "ПАВЛОВ СЕРГЕЙ СЕРГЕЕВИЧ",
    )
    authors_list = [Author(fio=x) for x in authors_fio]
    for author in authors_list:
        db.session.add(author)

    books_data = (
        ("СБРОНИК ЗАДАЧ ПО МАТЕМАТИКЕ", 199),
        ("СБОРНИК ЗАДАЧ ПО ФИЗИКЕ", 321),
        ("СБОРНИК РАССКАЗОВ", 231),
        ("ЛИТЕРАТУРА", 222),
        ("КОМПЬЮТЕРНЫЕ СЕТИ", 731)
    )
    books_list = [Book(name=x, pages_num=y) for x, y in books_data]
    for book in books_list:
        db.session.add(book)

    db.session.commit()
    yield db
    db.session.remove()
    db.drop_all()


def test_books_empty_list(testing_client, init_database):
    response = testing_client.get("/api/books?authors=yes")
    assert response.status_code == 200
    assert response.json == {'books': []}

def test_books_detail_first_book(testing_client, init_database):
    response = testing_client.get("/api/books?authors=yes")
    assert response.status_code == 200
    assert response.json == {'books': [
        {
            'name': 'СБРОНИК ЗАДАЧ ПО МАТЕМАТИКЕ',
            'pages_num': 199
        }
    ]}


def test_api_authors_not_empty_list(testing_client, init_database):
    response = testing_client.get("/api/authors")
    assert response.status_code == 200
    assert response.data != b'{"authors":[]}\n'
