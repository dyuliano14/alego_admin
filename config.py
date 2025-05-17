import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'segredo-super-seguro')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///alego_admin.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'output', 'disciplinas')
