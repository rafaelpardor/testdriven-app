import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS

db = SQLAlchemy()
toolbar = DebugToolbarExtension()


def create_app(script_info=None):
    app = Flask(__name__)
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    CORS(app)

    db.init_app(app)
    toolbar.init_app(app)

    from project.api.users import users_blueprint

    app.register_blueprint(users_blueprint)

    app.shell_context_processor({'app': app, 'db': db})
    return app
