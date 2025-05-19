import os

class Config:
    SECRET_KEY = 'sua-chave-secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///alego_admin.db'  # ✅ Aqui!
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'seuemail@gmail.com'
    MAIL_PASSWORD = 'suasenhadeaplicativo'
