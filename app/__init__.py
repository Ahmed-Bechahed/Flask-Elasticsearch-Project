from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    from .routes import main
    app.register_blueprint(main)

    return app
