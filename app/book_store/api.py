from book_store.schema import (
    AuthorSchema, BookSchema, Author, Book, db
)
from flask import request


class BookViewAPI:
    book_schema = BookSchema()

    @classmethod
    def books_list(cls):
        filter_authors = request.args.get(
            'authors',
            default='yes',
            type=str
        )
        if filter_authors == 'yes':
            books = Book.query.where(Book.authors)
        else:
            books = Book.query.filter(Book.authors == None)
        cls.book_schema.many = True
        result = cls.book_schema.dump(books)
        return {"books": result}

    @classmethod
    def book_detail(cls, pk):
        try:
            get_book = Book.query.get(pk)
            cls.book_schema.many = False
            result = cls.book_schema.dump(get_book)
            return {"book": result}
        except Exception as e:
            return {'message': str(e)}, 400

    @classmethod
    def new_book(cls):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # load_instance = True -- Атрибут, ответственный за десереализацию
        # в объект модели, требует активной сессии
        session = db.session
        cls.book_schema.many = False

        # Удаляем список значений id авторов из словаря, чтобы book_schema не
        # десериализовала поле вне схемы. Ищем авторов в БД и заносим в
        # список
        authors = []
        authors_obj_list = []
        if 'authors' in json_data:
            authors = [x for x in json_data['authors']]
            del json_data['authors']
            authors_obj_list = Author.query.filter(
                Author.id.in_(authors)
            ).all()

        book = cls.book_schema.load(json_data, session=session)

        # Если авторы из словаря нашлись, то привязываем их к книге
        if len(authors_obj_list) > 0:
            for author in authors_obj_list:
                book.authors.append(author)

        result = cls.book_schema.dump(book.create())
        return {"message": "Created new book", "book": result}

    @classmethod
    def update_book(cls, pk):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            get_book = Book.query.get(pk)
            for key, val in json_data.items():
                if hasattr(get_book, key):
                    setattr(get_book, key, val)
            cls.book_schema.many = False
            db.session.add(get_book)
            db.session.commit()
            result = cls.book_schema.dump(get_book)
            return {
                "message": f"Updated book [id: {get_book.id}]",
                "book": result
            }
        except Exception as e:
            return {'message': str(e)}, 400

    @classmethod
    def delete_book(cls, pk):
        try:
            get_book = Book.query.get(pk)
            db.session.delete(get_book)
            db.session.commit()
            return {"message": f"Deleted book [id: {get_book.id}]"}, 204
        except Exception as e:
            return {'message': str(e)}, 400


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
            get_author = Author.query.get(pk)
            cls.author_schema.many = False
            result = cls.author_schema.dump(get_author)
            return {"author": result}
        except Exception as e:
            return {'message': str(e)}, 400

    @classmethod
    def new_author(cls):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        cls.author_schema.many = False
        session = db.session
        author = cls.author_schema.load(json_data, session=session)
        result = cls.author_schema.dump(author.create())
        return {"message": "Created new author", "author": result}

    @classmethod
    def update_author(cls, pk):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            get_author = Author.query.get(pk)
            for key, val in json_data.items():
                if hasattr(get_author, key):
                    setattr(get_author, key, val)
            cls.author_schema.many = False
            db.session.add(get_author)
            db.session.commit()
            result = cls.author_schema.dump(get_author)
            return {
                "message": f"Updated author [id: {get_author.id}]",
                "author": result
            }
        except Exception as e:
            return {'message': str(e)}, 400

    @classmethod
    def delete_author(cls, pk):
        try:
            get_author = Author.query.get(pk)
            db.session.delete(get_author)
            db.session.commit()
            return {"message": f"Deleted author [id: {get_author.id}]"}, 204
        except Exception as e:
            return {'message': str(e)}, 400
