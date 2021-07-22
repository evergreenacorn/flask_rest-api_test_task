from tests.test_app import Book, Author, testing_client, init_database


def test_author_list(testing_client, init_database):
    response = testing_client.get("/api/authors")
    assert response.status_code == 200
    assert len(response.json['authors']) == 5


def test_author_detail(testing_client, init_database): ...


def test_new_author(testing_client, init_database): ...


def test_update_author(testing_client, init_database): ...


def test_delete_author(testing_client, init_database): ...
