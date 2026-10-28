from app.routes.admin import admin_bp
from app.routes.auth import auth_bp
from app.routes.courses import courses_bp
from app.routes.enrollments import enrollments_bp
from app.routes.health import health_bp
from app.routes.lessons import lessons_bp
from app.routes.modules import modules_bp
from app.routes.progress import progress_bp
from app.routes.quizzes import quizzes_bp


def register_blueprints(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(modules_bp)
    app.register_blueprint(lessons_bp)
    app.register_blueprint(enrollments_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(quizzes_bp)
    app.register_blueprint(admin_bp)
