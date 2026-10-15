from app.extensions import db

# PostgreSQL uses BIGINT; SQLite uses INTEGER so reference tests can autogenerate PKs.
BIGINT = db.BigInteger().with_variant(db.Integer, "sqlite")


class TimestampMixin:
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now(),
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )
