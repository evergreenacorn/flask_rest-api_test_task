from book_store.views import (
    BookViewAPI, AuthorViewAPI,
    BookAPIView, AuthorAPIView
)

import inspect


class BookRules:
    book_api = BookViewAPI

    @classmethod
    def add_book_list_rule(cls, app):
        app.add_url_rule(
            '/api/books',
            methods=['GET'],
            view_func=cls.book_api.books_list)

    @classmethod
    def add_book_detail_rule(cls, app):
        app.add_url_rule(
            '/api/books/<int:pk>',
            methods=['GET'],
            view_func=cls.book_api.book_detail)

    @classmethod
    def add_new_book_rule(cls, app):
        app.add_url_rule(
            '/api/books',
            methods=['POST'],
            view_func=cls.book_api.new_book)

    @classmethod
    def add_update_book_rule(cls, app):
        app.add_url_rule(
            '/api/books/<int:pk>',
            methods=['PUT'],
            view_func=cls.book_api.update_book)

    @classmethod
    def add_delete_book_rule(cls, app):
        app.add_url_rule(
            '/api/books/<int:pk>',
            methods=['DELETE'],
            view_func=cls.book_api.delete_book)


class AuthorRules:
    author_api = AuthorViewAPI

    @classmethod
    def add_author_list_rule(cls, app):
        app.add_url_rule(
            '/api/authors',
            methods=['GET'],
            view_func=cls.author_api.authors_list)

    @classmethod
    def add_author_detail_rule(cls, app):
        app.add_url_rule(
            '/api/authors/<int:pk>',
            methods=['GET'],
            view_func=cls.author_api.author_detail)

    @classmethod
    def add_new_author_rule(cls, app):
        app.add_url_rule(
            '/api/authors',
            methods=['POST'],
            view_func=cls.author_api.new_author)

    @classmethod
    def add_update_author_rule(cls, app):
        app.add_url_rule(
            '/api/authors/<int:pk>',
            methods=['PUT'],
            view_func=cls.author_api.update_author)

    @classmethod
    def add_delete_author_rule(cls, app):
        app.add_url_rule(
            '/api/authors/<int:pk>',
            methods=['DELETE'],
            view_func=cls.author_api.delete_author)


def register_api(app, view, url, pk='id', pk_type='int'):
    app.add_url_rule(
        url, default={pk: None}, view_func=view, methods=['GET']
    )
    app.add_url_rule(url, view_func=view, methods=['POST'])
    app.add_url_rule(
        f"{url}<{pk_type}:{pk}>", view_func=view,
        methods=['GET', 'PUT', 'DELETE']
    )


def configure_apis(app):
    apis_data = (
        (BookAPIView, '/books/', 'book_id', 'int'),
        (AuthorAPIView, '/authors/', 'author_id', 'int')
    )
    for api_view_class, url, pk, pk_type in apis_data:
        register_api(app, api_view_class, url, pk, pk_type)


def parse_class_rules(rules_class):
    """
        Функция возвращает список классовых методов,
        устанавливающих маршрут по url, название которых
        начинается с 'add_'.

        прим.: add_delete_author_rule
    """
    return [
        method[1] for method in inspect.getmembers(
            rules_class, predicate=inspect.ismethod
        ) if str(method[0]).startswith('add_')
    ]


def configure_routes(app):
    """
        Функция динамически генерирует списки методов
        для привязки маршрутов каждого API и вызывает их.
    """
    rules_classes = (BookRules, AuthorRules)
    rules = (parse_class_rules(rule_cls) for rule_cls in rules_classes)
    for class_rulls_list in rules:
        for rule in class_rulls_list:
            rule(app)
