import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    # SQLALCHEMY_DATABASE_URI = "postgresql://josue:2200166@localhost/eisi"
    # postgresql://eisidb_user:UyocTkkfv3ncOIp7whmXPlL1D7d1VVyE@dpg-ct5ub8d6l47c73frr2lg-a.oregon-postgres.render.com/eisidb
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # Llave para proteger formularios
