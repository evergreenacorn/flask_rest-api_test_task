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


# @pytest.fixture
@pytest.fixture(scope='module')
def testing_client():
    # db_fakedirectory, db_path = tempfile.mkstemp()

    # test_app = Flask(__name__)
    # test_app.config.from_object(TestConfig)
    # TestConfig.DATABASE = db_path
    # test_app = create_app(TestConfig)

    # db = SQLAlchemy()
    # migrate = Migrate()
    # ma = Marshmallow()

    # with test_app.test_client() as client:
    #     # with test_app.app_context():
    #         # db.init_app(test_app)
    #         # migrate.init_app(test_app, db)
    #         # ma.init_app(test_app)
    #     test_app.app_context().push()
    #     yield client

    # db_fakedirectory, db_path = tempfile.mkstemp()
    # TestConfig.DATABASE = TestConfig.DATABASE + db_path
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    TestConfig.SQLALCHEMY_DATABASE_URI = TestConfig.SQLALCHEMY_DATABASE_URI + \
        os.path.join(BASE_DIR, 'app.sqlite3')
    test_app = create_app(TestConfig)
    configure_routes(test_app)  # привязка маршрутов выполяется корректно
    testing_client = test_app.test_client()
    context = test_app.app_context()
    context.push()

    yield testing_client
    context.pop()

    # os.close(db_fakedirectory)
    # os.unlink(db_path)


@pytest.fixture(scope='module')
# @pytest.fixture
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
    books_list = [Book(name=x[0], pages_num=x[1]) for x in books_data]
    for book in books_list:
        db.session.add(book)

    db.session.commit()
    yield db
    db.drop_all()


# def test_empty_db(testing_client, init_database):
def test_api_books_empty_list(testing_client, init_database):
    response = testing_client.get("/api/books")
    assert response.status_code == 200
    assert response.data == b'{"books":[]}\n'


def test_api_authors_empty_list(testing_client, init_database):
    response = testing_client.get("/api/authors")
    assert response.status_code == 200
    assert response.data == b'{"authors":[]}\n'
