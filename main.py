from dotenv import load_dotenv

from models.user import User

load_dotenv()

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

from flask import Flask
from flask_login import LoginManager
from configs.db import Config,db, migrate

from endpoints.routes import main_bp

login_manager = LoginManager()
login_manager.login_view = "main.login_view"  # route login default

UPLOAD_FOLDER = None 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db) #development, jangan gunakan pada production
    csrf.init_app(app) 
    login_manager.init_app(app) 
    app.register_blueprint(main_bp)

    return app

app = create_app()
