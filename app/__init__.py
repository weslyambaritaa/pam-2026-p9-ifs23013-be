from flask import Flask
from flask_cors import CORS
from app.extensions import Base, engine
from app.routes.football_routes import football_bp

def create_app():
    app = Flask(__name__)
    
    # enable cros
    CORS(app)

    # create tables
    Base.metadata.create_all(bind=engine)

    # register blueprint
    app.register_blueprint(football_bp)

    return app