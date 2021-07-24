from book_store.models import Book, Author, db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, fields


class AuthorSchema(SQLAlchemyAutoSchema):
    """
        Класс схемы(аналог сериализатора drf) модели Author
    """

    class Meta:
        model = Author
        include_fk = True
        load_instance = True  # десереализация в экземпляр модели


class BookSchema(SQLAlchemyAutoSchema):
    """
        Класс схемы(аналог сериализатора drf) модели Book
    """
    authors = fields.Nested(AuthorSchema(many=True, exclude=('book_id',)))

    class Meta:
        model = Book
        include_relationships = True
        load_instance = True
