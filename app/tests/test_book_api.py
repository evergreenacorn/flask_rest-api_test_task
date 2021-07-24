from tests.test_app import (
    Book, Author,
    testing_client, init_database,
)


def test_books_list_w_authors(testing_client, init_database):
    response = testing_client.get("/api/books?authors=yes")
    assert response.status_code == 200
    assert len(response.json['books']) == 2


def test_books_list_no_authors(testing_client, init_database):
    response = testing_client.get("/api/books?authors=no")
    assert response.status_code == 200
    assert len(response.json['books']) == 3


def test_book_detail_first(testing_client, init_database):
    response = testing_client.get("/api/books/1")
    first_book = Book.query.get(1)
    assert response.status_code == 200
    assert response.json['book']['name'] == first_book.name
    assert response.json['book']['pages_num'] == first_book.pages_num


def test_new_book(testing_client, init_database):
    mimetype = "application/json"
    headers = {'Content-Type': mimetype, 'Accept': mimetype}
    data = {
        "name": "АЛГОРИТМЫ И СТРУКТУРЫ ДАННЫХ",
        "pages_num": 992,
    }
    response = testing_client.post(
        "/api/books",
        json=data,
        headers=headers)
    assert response.status_code == 200
    assert response.json['message'] == "Created new book"


def test_new_book_w_authors(testing_client, init_database):
    mimetype = "application/json"
    headers = {'Content-Type': mimetype, 'Accept': mimetype}
    data = {
        "name": "АЛГОРИТМЫ И СТРУКТУРЫ ДАННЫХ. ЧАСТЬ 2",
        "pages_num": 997,
        "authors": [3]
    }
    response = testing_client.post(
        "/api/books",
        json=data,
        headers=headers)
    assert response.status_code == 200
    assert response.json['message'] == "Created new book"


def test_update_book(testing_client, init_database):
    updated_book = Book.query.get(1)
    data = {"book": {
        "id": updated_book.id,
        "name": updated_book.name,
        "pages_num": updated_book.pages_num,
        "created_at": updated_book.created_at,
        "updated_at": updated_book.updated_at,
        "authors": updated_book.authors
    }}
    data["name"] = "ЛОЛКЕКЧЕБУРЕК"
    mimetype = "application/json"
    headers = {'Content-Type': mimetype, 'Accept': mimetype}
    response = testing_client.put(
        "/api/books/1",
        json=data,
        headers=headers)
    assert response.status_code == 201
    assert response.json['message'] == f"Updated book [id: {updated_book.id}]"
    assert response.json['book']['name'] == "ЛОЛКЕКЧЕБУРЕК"


def test_delete_book(testing_client, init_database):
    deleted_book = Book(name="УДАЛИ МЕНЯ", pages_num=111).update_or_create()
    data = {"book": {
        "id": deleted_book.id,
        "name": deleted_book.name,
        "pages_num": deleted_book.pages_num,
        "created_at": deleted_book.created_at,
        "updated_at": deleted_book.updated_at,
        "authors": deleted_book.authors
    }}
    mimetype = "application/json"
    headers = {'Content-Type': mimetype, 'Accept': mimetype}
    response = testing_client.delete(
        "/api/books/1",
        json=data,
        headers=headers)
    assert response.status_code == 200
