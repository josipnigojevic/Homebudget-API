from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager
from .config import Config


db  = SQLAlchemy()
jwt = JWTManager()

SWAGGER_URL = "/apidocs"
API_JSON    = "/static/swagger.json"

def create_app(config: dict | None = None):
    app = Flask(__name__)

    app.config.from_object(Config)
    if config:
        app.config.update(config)

    db.init_app(app)
    jwt.init_app(app)

    app.config["JWT_VERIFY_SUB"]        = False
    app.config["JWT_ERROR_MESSAGE_KEY"] = "message"

    @jwt.unauthorized_loader
    def missing_token(reason):
        return jsonify({"message": reason}), 401

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return jsonify({"message": reason}), 401

    @jwt.expired_token_loader
    def expired_token(header, payload):
        return jsonify({"message": "Token has expired"}), 401

    from .routes.auth     import auth_bp
    from .routes.category import category_bp
    from .routes.expense  import expense_bp

    app.register_blueprint(auth_bp,      url_prefix="/auth")
    app.register_blueprint(category_bp,  url_prefix="/categories")
    app.register_blueprint(expense_bp,   url_prefix="/expenses")

    swagger_ui_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_JSON,
        config={"app_name": "HomeBudget API"}
    )
    app.register_blueprint(swagger_ui_bp, url_prefix=SWAGGER_URL)

    with app.app_context():
        db.create_all()

    return app
