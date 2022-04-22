from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)

    from .routes import planets_bp
    app.register_blueprint(planets_bp)

<<<<<<< HEAD
=======

>>>>>>> aaded4f914e3e01131f9ae5cf6ff2b26ce272db8
    return app


