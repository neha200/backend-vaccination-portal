from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from db import mongo

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    JWTManager(app)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    # Import and register routes
    from routes.auth import auth_bp
    from routes.admin_routes import admin_bp
    from routes.drives import drive_bp
    from routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(drive_bp)
    app.register_blueprint(dashboard_bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

