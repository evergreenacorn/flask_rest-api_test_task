from book_store import create_app, db
from book_store.models import Author, Book


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Author': Author,
        'Book': Book
    }
