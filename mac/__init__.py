# Application set up taken directly from:
# https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/

import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # A default secret key that should be overridden by instance config
        SECRET_KEY="dev",
        # Store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "my-anime-collection.sqlite"),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in
        app.config.update(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Import initialize_app() to register database functions with application instance
    from . import db
    db.initialize_app(app)

    # Import and register the "auth" blueprint
    from . import auth
    app.register_blueprint(auth.blueprint)

    from . import collection
    app.register_blueprint(collection.blueprint)
    app.add_url_rule("/", endpoint="index")

    return app
