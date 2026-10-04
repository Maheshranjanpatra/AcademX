from flask import Flask, request, redirect, url_for, session, flash, render_template
from flask_login import current_user
from app.config import Config
from app.extensions import db, migrate, login_manager, oauth, csrf
from datetime import date


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ---- Extensions ----
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    oauth.init_app(app)
    csrf.init_app(app)

    google = oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    # ---- Models ----
    from app.models import user, question, quiz, video, paper, material

    @login_manager.user_loader
    def load_user(user_id):
        return user.User.query.get(int(user_id))

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

    # ---- Global before_request ----
    @app.before_request
    def enforce_profile_completion():
        if request.endpoint == 'static' or request.path.startswith('/static/'):
            return

        PUBLIC_ENDPOINTS = [
            'auth.index',
            'auth.login',
            'auth.admin_login',
            'auth.login_google',
            'auth.callback',
            'pages.about',
            'pages.contact',
            'pages.policy',
            'auth.complete_profile',
            'pages.ping',
        ]

        if current_user.is_authenticated and not current_user.profile_complete:
            if request.endpoint not in ['auth.complete_profile', 'auth.logout']:
                flash("Please complete your profile first.", "error")
                return redirect(url_for('auth.complete_profile'))

        if not current_user.is_authenticated and request.endpoint not in PUBLIC_ENDPOINTS:
            return redirect(url_for('auth.login'))

    # ---- Context processors ----
    @app.context_processor
    def inject_streak_status():
        if not current_user.is_authenticated:
            return {"streak_warning": False}

        streak = getattr(current_user, "streak", None)
        if streak and streak.last_completed_date:
            gap = (date.today() - streak.last_completed_date).days
            if gap == 2:
                return {"streak_warning": True}

        return {"streak_warning": False}

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
