from book_store.schema import (
    AuthorSchema, BookSchema, Author, Book
)
from flask import request, jsonify, make_response
from flask.views import MethodView


class BookViewAPI:
    book_schema = BookSchema()

    @classmethod
    def books_list(cls):
        books = Book.query.all()
        cls.book_schema.many = True
        result = cls.book_schema.dump(books)
        return {"books": result}

    @classmethod
    def book_detail(cls, pk):
        try:
            book_by_id = Book.query.filter(Book.id == pk).one()
            cls.book_schema.many = False
            result = cls.book_schema.dump(book_by_id)
            return {"book": result}
        except Exception as e:
            return {'message': str(e)}, 400

    @classmethod
    def new_book(cls, **kwargs):
        json_data = request.get_json()
        cls.book_schema.many = False
        book, error = cls.book_schema.load(json_data)
        result = cls.book_schema.dump(Book.create()).data
        return make_response(jsonify({"books": book}), 201)


class AuthorViewAPI:
    author_schema = AuthorSchema()

    @classmethod
    def authors_list(cls):
        authors = Author.query.all()
        cls.author_schema.many = True
        result = cls.author_schema.dump(authors)
        return {"authors": result}

    @classmethod
    def author_detail(cls, pk):
        try:
            author = Author.query.filter(Author.id == pk).one()
            cls.author_schema.many = False
            result = cls.author_schema.dump(author)
            return {"author": result}
        except Exception as e:
            return {'message': str(e)}, 400
