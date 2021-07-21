from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.app import Flask
from config import TestConfig
from flask import Flask
# from flaskr.db import ini_db
import tempfile
import pytest
import os


@pytest.fixture
def client():
    db_fakedirectory, db_path = tempfile.mkstemp()

    test_app = Flask(__name__)
    test_app.config.from_object(TestConfig)
    test_app.config['DATABASE'] = db_path

    db = SQLAlchemy()
    migrate = Migrate()
    ma = Marshmallow()

    with test_app.test_client() as client:
        with test_app.app_context():
            db.init_app(test_app)
            migrate.init_app(test_app, db)
            ma.init_app(test_app)
        yield client

    os.close(db_fakedirectory)
    os.unlink(db_path)
