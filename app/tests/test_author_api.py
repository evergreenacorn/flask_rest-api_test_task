from tests.test_app import (
    Book, Author,
    testing_client, init_database,
)


def test_author_list(testing_client, init_database):
    response = testing_client.get("/api/authors")
    assert response.status_code == 200
    assert len(response.json['authors']) == 5


def test_author_detail_first(testing_client, init_database):
    response = testing_client.get("/api/authors/1")
    first_author = Author.query.get(1)
    assert response.status_code == 200
    assert response.json['author']['fio'] == first_author.fio


def test_new_author(testing_client, init_database):
    mimetype = "application/json"
    headers = {'Content-Type': mimetype, 'Accept': mimetype}
    data = {
        "fio": "ПЕТРОВ ИВАН КУЗЬМИЧ"
    }
    response = testing_client.post(
        "/api/authors",
        json=data,
        headers=headers)
    assert response.status_code == 200
    assert response.json['message'] == "Created new author"


def test_update_author(testing_client, init_database):
    updated_author = Author.query.get(1)
    data = {"author": {
        "id": updated_author.id,
        "fio": updated_author.fio,
        "book_id": updated_author.book_id,
        "created_at": updated_author.created_at,
        "updated_at": updated_author.updated_at
    }}
    data["fio"] = "ИВАНОВ СТЕПАН ИГНАТЬЕВИЧ"
    mimetype = "application/json"
    headers = {'Content-Type': mimetype, 'Accept': mimetype}
    response = testing_client.put(
        "/api/authors/1",
        json=data,
        headers=headers)
    assert response.status_code == 200
    assert response.json['message'] == f"Updated author [id: {updated_author.id}]"
    assert response.json['author']['fio'] == "ИВАНОВ СТЕПАН ИГНАТЬЕВИЧ"


def test_delete_author(testing_client, init_database):
    deleted_author = Author(fio="ДЯДЯ СТЕПА СВЕТОФОР").create()
    data = {"author": {
        "id": deleted_author.id,
        "fio": deleted_author.fio,
        "book_id": deleted_author.book_id,
        "created_at": deleted_author.created_at,
        "updated_at": deleted_author.updated_at
    }}
    mimetype = "application/json"
    headers = {'Content-Type': mimetype, 'Accept': mimetype}
    response = testing_client.delete(
        "/api/authors/1",
        json=data,
        headers=headers)
    assert response.status_code == 204
