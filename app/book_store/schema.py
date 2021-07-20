from book_store.models import Book, Author
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
# from book_store import ma


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
    class Meta:
        model = Book
        include_relationships = True
        load_instance = True
