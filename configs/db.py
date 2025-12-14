import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.pool import NullPool

db = SQLAlchemy()
migrate = Migrate()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key-34279ds78g72352hf78#dfgf")
    #SQLALCHEMY_DATABASE_URI = (
    #    f"postgresql+psycopg://{os.environ.get('POSTGRES_USER')}:"
    #    f"{os.environ.get('POSTGRES_PASSWORD')}@"
    #    f"{os.environ.get('POSTGRES_HOST')}:"
    #    f"{os.environ.get('POSTGRES_PORT')}/"
    #    f"{os.environ.get('POSTGRES_DB')}"
    #)

    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRES_DATABASE_URL") 

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
    "connect_args": {"sslmode": "require"},  
    "poolclass": NullPool # serveles database
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
 