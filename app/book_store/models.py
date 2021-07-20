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
        DateTime,
        default=func.current_timestamp(),
    )
    updated_at = Column(
        DateTime,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )


class Author(StandartModelMixin, TimestampMixin, db.Model):
    fio = Column(String, nullable=False)
    book_id = Column(
        Integer,
        ForeignKey("book.id", ondelete='cascade'),
        nullable=True)
    books = relationship("Book", backref="authors")

    def __init__(self, fio, books=None):
        self.fio = fio
        self.books = books

    def __repr__(self):
        return '<Author %d>' % self.id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class Book(StandartModelMixin, TimestampMixin, db.Model):
    name = Column(String, nullable=False)
    pages_num = Column(Integer, nullable=False)

    def __init__(self, name, pages_num):
        self.name = name
        self.pages_num = pages_num

    def __repr__(self):
        return '<Book %d>' % self.id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
