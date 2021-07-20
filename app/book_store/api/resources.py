from flask_restful import Resource, reqparse
from book_store.models import Book, Author


class AuthorResource(Resource):
    def get(self, author_id=None):
        """
            List, detail queries
        """
        if author_id is None:
            authors = Author.query.all()
            return authors, 200
        try:
            author = Author.query.get(author_id)
            return author, 200
        except Exception as e:
            return e, 404

    def post(self, author_id):
        """
            Create query
        """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("fio")
            parser.add_argument("quote")
            params = parser.parse_args()
            updated_author = None
            return updated_author, 200
        except Exception as e:
            return e, 404

    def put(sef, author_id):
        """
            Update query
        """
        pass

    def delete(self, author_id):
        """
            Delete query
        """
        pass


class BookResource(Resource):
    def get(self, book_id=None):
        if book_id is None:
            books = Book.query.all()
            return books, 200
        try:
            book = Book.query.get(book_id)
            return book, 200
        except Exception as e:
            return e, 404

    def post(self, book_id): ...

    def put(sef, book_id): ...

    def delete(self, book_id): ...
