import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://josue:2200166@localhost/eisi"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # Llave para proteger formularios
