import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.sqlite3')
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    TESTING = True
    DATABASE = None
