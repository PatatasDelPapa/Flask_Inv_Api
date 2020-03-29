from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flasksystem.config import Config
from flask_migrate import Migrate, MigrateCommand
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
ma = Marshmallow()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from flasksystem.main.routes import main
from flasksystem.materias.routes import materias
from flasksystem.reactivos.routes import reactivos
from flasksystem.users.routes import users
from flasksystem.errors.handlers import errors


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(materias)
    app.register_blueprint(reactivos)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    return app
