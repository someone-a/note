from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from note.db import db
from note.user.models import User
from note.user.views import blueprint as user_blueprint
from note.note.views import blueprint as note_blueprint
from note.api.views import blueprint as api_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    migrate = Migrate(app, db)
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(user_blueprint)
    app.register_blueprint(note_blueprint)
    app.register_blueprint(api_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


    return app
