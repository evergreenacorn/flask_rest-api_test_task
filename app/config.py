from os import getenv
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = getenv('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.sqlite3')
    DEBUG = getenv("DEBUG") or True
    SQLALCHEMY_TRACK_MODIFICATIONS = getenv("SQLALCHEMY_TRACK_MODIFICATIONS") or False


class TestConfig:
    SECRET_KEY = 'bad_secret_keyedfcvdswed'
    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app_test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
