from book_store.api import BookViewAPI, AuthorViewAPI
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


def configure_routes(app):
    """
        Функция динамически генерирует списки методов
        для привязки маршрутов каждого API и вызывает их.
        p.s.
        Очень хотелось поюзать интроспекцию и динамически
        собрать списки классовых методов
    """
    book_rules = [
        method[1] for method in inspect.getmembers(
            BookRules, predicate=inspect.ismethod
        ) if str(method[0]).startswith('add_')
    ]
    author_rules = [
        method[1] for method in inspect.getmembers(
            AuthorRules, predicate=inspect.ismethod
        ) if str(method[0]).startswith('add_')
    ]
    rules = book_rules + author_rules
    for rule in rules:
        rule(app)
