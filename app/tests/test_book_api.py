from tests.test_app import Book, Author, testing_client, init_database


def test_books_list_w_authors(testing_client, init_database):
    response = testing_client.get("/api/books?authors=yes")
    assert response.status_code == 200
    assert len(response.json['books']) == 2


def test_books_list_no_authors(testing_client, init_database):
    response = testing_client.get("/api/books?authors=no")
    assert response.status_code == 200
    assert len(response.json['books']) == 3


def test_book_detail_first_list(testing_client, init_database):
    response = testing_client.get("/api/books/1")
    try:
        first_book = Book.query.get(1)
        assert response.status_code == 200
        assert response.json['book']['name'] == first_book.name
        assert response.json['book']['pages_num'] == first_book.pages_num
    except Exception as e:
        raise e


def test_new_book(testing_client, init_database):
    pass


def test_new_book_w_authors(testing_client, init_database): ...


def test_update_book(testing_client, init_database): ...


def test_delete_book(testing_client, init_database): ...
