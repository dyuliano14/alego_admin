import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua_chave_secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///alego_admin.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
