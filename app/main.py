from book_store import create_app, db
from book_store.models import Author, Book
from book_store.api import BookViewAPI, AuthorViewAPI


app = create_app()
# Book API
# get all books
app.add_url_rule(
    '/api/books',
    methods=['GET'],
    view_func=BookViewAPI.books_list)

# get book by id
app.add_url_rule(
    '/api/books/<int:pk>',
    methods=['GET'],
    view_func=BookViewAPI.book_detail)

# create new book
app.add_url_rule(
    '/api/books',
    methods=['POST'],
    view_func=BookViewAPI.new_book)

# update book
app.add_url_rule(
    '/api/books/<int:pk>',
    methods=['PUT'],
    view_func=BookViewAPI.update_book)

# update book
app.add_url_rule(
    '/api/books/<int:pk>',
    methods=['DELETE'],
    view_func=BookViewAPI.delete_book)


# Author API
# get all authors
app.add_url_rule(
    '/api/authors',
    methods=['GET'],
    view_func=AuthorViewAPI.authors_list)

# get author by id
app.add_url_rule(
    '/api/authors/<int:pk>',
    methods=['GET'],
    view_func=AuthorViewAPI.author_detail)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Author': Author,
        'Book': Book
    }
