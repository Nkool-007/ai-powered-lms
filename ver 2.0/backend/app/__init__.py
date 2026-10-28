import click

from flask import Flask
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.security import generate_password_hash

from app.config import Config
from app.extensions import db, jwt, migrate
from app.utils.responses import error
from app.utils.validators import normalize_email, valid_email


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    app.config["FRONTEND_ORIGIN"]
                ],
                "allow_headers": [
                    "Content-Type",
                    "Authorization",
                ],
                "methods": [
                    "GET",
                    "POST",
                    "PUT",
                    "PATCH",
                    "DELETE",
                    "OPTIONS",
                ],
            }
        },
    )

    # Import all models so SQLAlchemy / Flask-Migrate discovers them.
    from app import models  # noqa: F401
    from app.routes import register_blueprints

    register_blueprints(app)

    @jwt.unauthorized_loader
    def missing_token(reason):
        return error(
            "AUTHENTICATION_REQUIRED",
            "Authentication is required.",
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return error(
            "INVALID_TOKEN",
            "Authentication token is invalid.",
            401,
        )

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return error(
            "TOKEN_EXPIRED",
            "Authentication token has expired.",
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token(jwt_header, jwt_payload):
        return error(
            "TOKEN_REVOKED",
            "Authentication token is no longer valid.",
            401,
        )

    @app.errorhandler(404)
    def not_found(exception):
        return error(
            "RESOURCE_NOT_FOUND",
            "Requested resource does not exist.",
            404,
        )

    @app.errorhandler(405)
    def method_not_allowed(exception):
        return error(
            "METHOD_NOT_ALLOWED",
            "HTTP method is not allowed for this endpoint.",
            405,
        )

    @app.errorhandler(IntegrityError)
    def integrity_error(exception):
        db.session.rollback()
        app.logger.exception("Database integrity error")

        return error(
            "DATABASE_CONFLICT",
            "The request conflicts with existing data.",
            409,
        )

    @app.errorhandler(OperationalError)
    def database_unavailable(exception):
        db.session.rollback()
        app.logger.exception("Database operation failed")

        return error(
            "DATABASE_UNAVAILABLE",
            "Database service is temporarily unavailable.",
            503,
        )

    @app.errorhandler(500)
    def internal_server_error(exception):
        db.session.rollback()
        app.logger.exception("Unhandled application error")

        return error(
            "INTERNAL_SERVER_ERROR",
            "An unexpected server error occurred.",
            500,
        )

    @app.cli.command("create-admin")
    @click.option("--name", prompt=True)
    @click.option("--email", prompt=True)
    @click.option(
        "--password",
        prompt=True,
        hide_input=True,
        confirmation_prompt=True,
    )
    def create_admin(name, email, password):
        from app.models import User

        email = normalize_email(email)

        if not valid_email(email):
            raise click.ClickException(
                "A valid email address is required."
            )

        if len(password) < 8:
            raise click.ClickException(
                "Password must contain at least 8 characters."
            )

        if User.query.filter_by(email=email).first():
            raise click.ClickException(
                "An account with this email already exists."
            )

        user = User(
            name=name.strip(),
            email=email,
            password_hash=generate_password_hash(password),
            role="ADMIN",
            is_active=True,
        )

        db.session.add(user)
        db.session.commit()

        click.echo(
            f"Admin created successfully: {user.email}"
        )

    return app
