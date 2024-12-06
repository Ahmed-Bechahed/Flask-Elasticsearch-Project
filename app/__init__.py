from flask import Flask
import secrets


def create_app():
    app = Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    app.secret_key = secrets.token_hex(16)  # Generates a random 32-character string


    from .routes import main
    app.register_blueprint(main)

    return app
