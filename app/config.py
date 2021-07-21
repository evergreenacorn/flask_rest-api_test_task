import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRES_DB', '').replace(
    #     'postgres://', 'postgresql://') or \
    #     'sqlite:///' + os.path.join(BASE_DIR, 'app.sqlite3')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.sqlite3')
    DEBUG = os.environ.get("DEBUG") or True
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    ) or False


class TestConfig:
    TESTING = True
    DATABASE = None
