"""Initialize app."""
from flask import Flask


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config['SECRET_KEY'] = 'dunno'
    # Application Configuration

    with app.app_context():
        # Import parts of our application
        from . import auth

        # Register Blueprints
        app.register_blueprint(auth.auth_bp)

        return app
