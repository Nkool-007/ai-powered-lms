from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models import User
from app.services.authorization import get_current_user
from app.utils.responses import error, success
from app.utils.validators import normalize_email, required_string, valid_email

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/v1/auth",
)


@auth_bp.post("/register")
def register():
    payload = request.get_json(silent=True) or {}

    name = payload.get("name")
    email = normalize_email(payload.get("email"))
    password = payload.get("password")
    role = str(payload.get("role", "STUDENT")).upper()

    if not required_string(name):
        return error(
            "VALIDATION_ERROR",
            "Name is required.",
            400,
            {"name": "Name cannot be empty."},
        )

    if not valid_email(email):
        return error(
            "VALIDATION_ERROR",
            "A valid email address is required.",
            400,
            {"email": "Invalid email address."},
        )

    if not isinstance(password, str) or len(password) < 8:
        return error(
            "VALIDATION_ERROR",
            "Password must contain at least 8 characters.",
            400,
        )

    if role not in {"STUDENT", "INSTRUCTOR"}:
        return error(
            "INVALID_ROLE",
            "Public registration supports STUDENT or INSTRUCTOR accounts.",
            400,
        )

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return error(
            "EMAIL_ALREADY_REGISTERED",
            "An account with this email already exists.",
            409,
        )

    user = User(
        name=name.strip(),
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
    )

    db.session.add(user)
    db.session.commit()

    return success(user.to_dict(), 201)


@auth_bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}

    email = normalize_email(payload.get("email"))
    password = payload.get("password")

    if not email or not isinstance(password, str):
        return error(
            "VALIDATION_ERROR",
            "Email and password are required.",
            400,
        )

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return error(
            "INVALID_CREDENTIALS",
            "Invalid email or password.",
            401,
        )

    if not user.is_active:
        return error(
            "ACCOUNT_DISABLED",
            "This account has been disabled.",
            403,
        )

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role},
    )

    return success(
        {
            "access_token": token,
            "user": user.to_dict(),
        }
    )


@auth_bp.get("/me")
@jwt_required()
def me():
    user = get_current_user()

    if not user:
        return error(
            "USER_NOT_FOUND",
            "Authenticated user does not exist.",
            401,
        )

    if not user.is_active:
        return error(
            "ACCOUNT_DISABLED",
            "This account has been disabled.",
            403,
        )

    return success(user.to_dict())
