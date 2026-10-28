# Merge into the existing backend/app/routes/__init__.py.
# Keep all existing blueprint imports and registrations.

from app.routes.ai import ai_bp

# Inside register_blueprints(app):
app.register_blueprint(ai_bp)
