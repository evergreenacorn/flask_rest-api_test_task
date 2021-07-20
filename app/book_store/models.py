from sqlalchemy import (
    Column, DateTime, ForeignKey, Integer,
    String, func, Table
)
from sqlalchemy.orm import (
    backref, relationship, declarative_mixin,
    declared_attr
)
from datetime import datetime
from book_store import db


@declarative_mixin
class StandartModelMixin:
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class TimestampMixin:
    created_at = Column(
        DateTime, nullable=False,
    )


association_table = Table(
    'book_identifier', db.Model.metadata,
    Column('author_id', Integer, ForeignKey('author.id'), nullable=True),
    Column('book_id', Integer, ForeignKey('book.id'), nullable=True)
)


class Author(StandartModelMixin, TimestampMixin, db.Model):
    fio = Column(String, nullable=False)
    books = relationship(
        "Book",
        secondary=association_table,
        back_populates="authors",
        # nullable=True
    )


class Book(StandartModelMixin, TimestampMixin, db.Model):
    name = Column(String, nullable=False)
    pages_num = Column(Integer, nullable=False)
    relationship(
        "Author",
        secondary=association_table,
        back_populates="books",
        # nullable=True
    )
