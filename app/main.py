from book_store import create_app, db
from book_store.models import Author, Book
from book_store.api import BookViewAPI, AuthorViewAPI
# from book_store.api import book_list, detail


app = create_app()
app.add_url_rule(
    '/api/books',
    methods=['GET'],
    view_func=BookViewAPI.books_list)

app.add_url_rule(
    '/api/books/<int:pk>',
    methods=['GET'],
    view_func=BookViewAPI.book_detail)


app.add_url_rule(
    '/api/books/',
    methods=['POST'],
    view_func=BookViewAPI.new_book)


app.add_url_rule(
    '/api/authors',
    methods=['GET'],
    view_func=AuthorViewAPI.authors_list)


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
