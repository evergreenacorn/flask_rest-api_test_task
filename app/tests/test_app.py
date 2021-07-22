from config import TestConfig
import pytest
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
    # 3 книги без авторов
    for book in books_list[2:]:
        db.session.add(book)
    # 2 книги с авторами
    for book, author in zip(books_list[:2], authors_list[:2]):
        book.authors.append(author)
        db.session.add(book)

    db.session.commit()
    yield db
    db.session.remove()
    db.drop_all()
