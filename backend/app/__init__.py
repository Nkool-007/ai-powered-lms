import click

from flask import Flask
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app.config import Config
from app.extensions import db, jwt, migrate
from app.utils.responses import error


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import every model so SQLAlchemy and Flask-Migrate discover them.
    from app import models  # noqa: F401
    from app.routes import register_blueprints

    register_blueprints(app)
    register_jwt_handlers()
    register_error_handlers(app)
    register_cli(app)

    return app


def register_jwt_handlers():
    @jwt.unauthorized_loader
    def missing_token(reason):
        return error(
            "AUTHENTICATION_REQUIRED",
            "A valid access token is required.",
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return error(
            "INVALID_TOKEN",
            "The access token is invalid.",
            401,
        )

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return error(
            "TOKEN_EXPIRED",
            "The access token has expired.",
            401,
        )


def register_error_handlers(app):
    @app.errorhandler(404)
    def route_not_found(exception):
        return error(
            "ROUTE_NOT_FOUND",
            "The requested API route does not exist.",
            404,
        )

    @app.errorhandler(IntegrityError)
    def database_integrity_error(exception):
        db.session.rollback()
        return error(
            "DATABASE_CONFLICT",
            "The requested operation conflicts with existing data.",
            409,
        )

    @app.errorhandler(500)
    def internal_error(exception):
        db.session.rollback()
        return error(
            "INTERNAL_SERVER_ERROR",
            "An unexpected server error occurred.",
            500,
        )


def register_cli(app):
    from app.models import User

    @app.cli.command("create-admin")
    @click.option("--name", prompt=True)
    @click.option("--email", prompt=True)
    @click.password_option()
    def create_admin(name, email, password):
        normalized_email = email.strip().lower()

        existing = User.query.filter_by(email=normalized_email).first()
        if existing:
            click.echo("User already exists.")
            return

        admin = User(
            name=name.strip(),
            email=normalized_email,
            password_hash=generate_password_hash(password),
            role="ADMIN",
        )

        db.session.add(admin)
        db.session.commit()
        click.echo("Admin created successfully.")
