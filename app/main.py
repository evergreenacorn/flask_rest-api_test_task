from book_store import create_app, db
from book_store.models import Author, Book
from book_store.routes import configure_routes


app = create_app()
configure_routes(app)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'app': app,
        'Author': Author,
        'Book': Book
    }
