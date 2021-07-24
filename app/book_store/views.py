from book_store.schema import (
    AuthorSchema, BookSchema, Author, Book, db
)
from flask import request, jsonify
from flask.views import MethodView
from marshmallow import ValidationError


class BookViewAPI:
    book_schema = BookSchema()

    @classmethod
    def books_list(cls):
        filter_authors = request.args.get(
            'authors',
            default='yes',
            type=str
        )
        if filter_authors == 'no':
            books = Book.query.filter(Book.authors == None)
        else:
            books = Book.query.where(Book.authors)
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

        result = cls.book_schema.dump(book.update_or_create())
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
            get_book.update_or_create()
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
            get_book.delete()
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
        result = cls.author_schema.dump(author.update_or_create())
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
            get_author.update_or_create()
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
            get_author.delete()
            return {"message": f"Deleted author [id: {get_author.id}]"}, 204
        except Exception as e:
            return {'message': str(e)}, 400


class BookAPIView(MethodView):
    model = Book
    schema = BookSchema

    def get(self, book_id):
        """
            Функция возвращает объект/список объектов Book
            в зависимости от наличия/отсутствия значения
            book_id отличного от None.
        """
        filter_by = "authors"
        filter_authors = request.args.get(
                filter_by,
                default='yes',
                type=str
        )
        if filter_authors == 'no':
            self.schema = self.schema(exclude=[filter_by])
        else:
            self.schema = self.schema()
        if book_id is not None:
            books = self.model.query.get_or_404(book_id)
            self.schema.many = False
        else:
            books = self.model.query.all()
            self.schema.many = True
        try:
            result = self.schema.dump(books)
            self.schema = BookSchema
            return jsonify(data=result), 200
        except Exception as e:
            return jsonify(errors=e), 404

    def post(self):
        """
            Функция создает новый экземпляр объекта Book
            и сохраняет его в сессии.
        """
        json_data = request.get_json()
        if not json_data:
            return jsonify(errors='No input data provided'), 204
        try:
            pass
        except ValidationError as e:  # ! Уточнить, при про ошибку валидации данных
            # ! пришедших с клиента
            return jsonify(errors=e.messages), 400
        except Exception as e:
            return jsonify(errors=e), 404

    def put(self, book_id):
        """
            Функция обновляет данные экземпляра объекта Book
            и сохраняет его в сессии.
        """
        json_data = request.get_json()
        if not json_data:
            return jsonify(errors='No input data provided'), 204
        pass

    def delete(self, book_id):
        """
            Функция удаляет экземпляр объекта Book из сессии.
        """
        book = self.model.query.get_or_404(book_id)
        self.model.delete()
        data = {"message": f"Deleted book [id: {book.id}]"}
        return jsonify(data=data), 200


class AuthorAPIView(MethodView):
    model = Author
    schema = AuthorSchema()

    def get(self, author_id):
        """
            Функция возвращает объект/список объектов Author
            в зависимости от наличия/отсутствия значения
            author_id отличного от None.
        """
        if author_id is not None:
            authors = self.model.query.get_or_404(author_id)
            self.schema.many = False
        else:
            authors = self.model.query.all()
            self.schema.many = True
        try:
            result = self.schema.dump(authors)
            return jsonify(data=result), 200
        except Exception as e:
            return jsonify(errors=e), 404

    def post(self): ...

    def put(self, author_id): ...

    def delete(self, author_id):
        author = self.model.query.get_or_404(author_id)
        self.model.delete()
        data = {"message": f"Deleted author [id: {author.id}]"}
        return jsonify(data=data), 200
