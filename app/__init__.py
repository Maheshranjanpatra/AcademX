from flask import Flask, request, redirect, url_for, session, flash
from flask_login import current_user
from app.config import Config
from app.extensions import db, migrate, login_manager, oauth, csrf
from datetime import date

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

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

    from app.models import user, question, quiz, video, paper, material

    @login_manager.user_loader
    def load_user(user_id):
        return user.User.query.get(int(user_id))

    # Register blueprints
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

    # GLOBAL BEFORE_REQUEST
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
        ]

        # user already logged in, profile not complete
        if current_user.is_authenticated and not current_user.profile_complete:
            if request.endpoint not in ['auth.complete_profile', 'auth.logout']:
                flash("Please complete your profile first.", "error")
                return redirect(url_for('auth.complete_profile'))
        if not current_user.is_authenticated and request.endpoint not in PUBLIC_ENDPOINTS:
            return redirect(url_for('auth.login'))
        return

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

    return app
