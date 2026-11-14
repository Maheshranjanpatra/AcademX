from flask import Flask, request, redirect, url_for, session, render_template
from flask_login import current_user
from app.config import Config
from app.extensions import db, migrate, login_manager, csrf
from datetime import date
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app(config_class=Config):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.config.from_object(config_class)
    secret_key = app.config.get("SECRET_KEY")
    if not isinstance(secret_key, str) or len(secret_key) < 32:
        raise RuntimeError("Set SECRET_KEY to a random value of at least 32 characters.")

    # ---- Extensions ----
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # ---- Models ----
    from app.models import user, question, quiz, video, paper, material, admin_login_attempt

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(user.User, int(user_id))
        except (TypeError, ValueError):
            return None

    # ---- Blueprints ----
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.qa import qa_bp
    from app.routes.quiz import quiz_bp
    from app.routes.video import video_bp
    from app.routes.paper import paper_bp
    from app.routes.materials import materials_bp
    from app.routes.admin import admin_bp
    from app.routes.pages import pages_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(qa_bp, url_prefix="/qa")
    app.register_blueprint(quiz_bp, url_prefix="/quiz")
    app.register_blueprint(video_bp, url_prefix="/video")
    app.register_blueprint(paper_bp, url_prefix="/papers")
    app.register_blueprint(materials_bp, url_prefix="/materials")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    # ---- Jinja filter for B2 signed URLs ----
    from app.utils.helpers import get_file_url
    app.jinja_env.filters["file_url"] = get_file_url

    # ---- Context processors ----
    @app.context_processor
    def inject_upload_limit():
        return {
            "MAX_UPLOAD_MB": app.config["MAX_CONTENT_LENGTH"] // (1024 * 1024)
        }

    # ---- Error handlers ----
    @app.errorhandler(500)
    def internal_error(error):
        try:
            db.session.rollback()
            return render_template('errors/500.html'), 500
        except Exception:
            return ("<h2>Something went wrong</h2>"
                    "<p>Please refresh in a few seconds.</p>"), 500

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return render_template('errors/413.html'), 413

    @app.before_request
    def redirect_old_domain():
        if request.host.startswith("nymora-anon.onrender.com"):
            new_url = request.url.replace(
                "nymora-anon.onrender.com",
                "academx.onrender.com",
                1
            )
            return redirect(new_url, code=301)

    return app
