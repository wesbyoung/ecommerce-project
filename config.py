import os
# from dotenv import load_dotenv
import dotenv

basedir = os.path.abspath(os.path.join(os.path.dirname(__name__), '.env'))
dotenv.load_dotenv(basedir)

class Config:
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY = os.getenv('SECRET_KEY')
# class Config:
#     FLASK_APP = 'run.py'
#     FLASK_ENV = 'development'
#     SQLALCHEMY_DATABASE_URI = 'postgres://hnqkajrb:bxnP9lEz13eQ6M3eU1izMjbZeaLyAJgd@lallah.db.elephantsql.com:5432/hnqkajrb
# '
    