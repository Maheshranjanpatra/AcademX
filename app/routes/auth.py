import hashlib
import hmac
import re
from datetime import datetime, timedelta, timezone

from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, session,
    url_for,
)
from flask_login import current_user, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.forms.admin_login import AdminLoginForm
from app.forms.auth import GuestLoginForm
from app.models.admin_login_attempt import AdminLoginAttempt
from app.models.question import Question
from app.models.user import User
from app.models.video import Playlist

auth_bp = Blueprint("auth", __name__)

ADMIN_LOGIN_WINDOW = timedelta(minutes=15)
ADMIN_LOGIN_MAX_ATTEMPTS = 5


def _guest_id_preview():
    candidate = session.get("guest_id_preview")
    if (
        isinstance(candidate, str)
        and re.fullmatch(r"User_\d{4}", candidate)
        and User.query.filter_by(anonymous_id=candidate).first() is None
    ):
        return candidate

    preview_user = User()
    preview_user.generate_anonymous_id()
    session["guest_id_preview"] = preview_user.anonymous_id
    return preview_user.anonymous_id


def _admin_login_address_hash():
    address = request.remote_addr or "unknown"
    key = current_app.config["SECRET_KEY"].encode("utf-8")
    return hmac.new(key, address.encode("utf-8"), hashlib.sha256).hexdigest()


@auth_bp.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for("admin.dashboard"))

    form = AdminLoginForm()
    if form.validate_on_submit():
        admin_username = current_app.config.get("ADMIN_USERNAME")
        admin_password = current_app.config.get("ADMIN_PASSWORD")
        if (
            not admin_username
            or not admin_password
            or not 3 <= len(admin_username) <= 50
            or len(admin_password) < 16
        ):
            current_app.logger.error(
                "Admin login is unavailable: credentials are missing or do not meet minimum requirements."
            )
            flash("Admin login is not securely configured. Please contact the site administrator.", "error")
            return render_template("admin/login.html", form=form), 503

        address_hash = _admin_login_address_hash()
        cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - ADMIN_LOGIN_WINDOW
        AdminLoginAttempt.query.filter(
            AdminLoginAttempt.attempted_at < cutoff
        ).delete(synchronize_session=False)
        recent_attempts = AdminLoginAttempt.query.filter(
            AdminLoginAttempt.address_hash == address_hash,
            AdminLoginAttempt.attempted_at >= cutoff,
        ).count()

        if recent_attempts >= ADMIN_LOGIN_MAX_ATTEMPTS:
            db.session.commit()
            flash("Too many failed attempts. Please wait 15 minutes before trying again.", "error")
            return render_template("admin/login.html", form=form), 429

        username_matches = hmac.compare_digest(form.username.data, admin_username)
        password_matches = hmac.compare_digest(form.password.data, admin_password)
        if username_matches and password_matches:
            admin_user = User.query.filter_by(is_admin=True).first()
            if not admin_user:
                admin_user = User(
                    name="Administrator",
                    is_admin=True,
                    profile_complete=True,
                    avatar="avatar1.webp",
                )
                db.session.add(admin_user)

            AdminLoginAttempt.query.filter_by(address_hash=address_hash).delete(
                synchronize_session=False
            )
            db.session.commit()
            session.clear()
            session.permanent = True
            login_user(admin_user, remember=False, fresh=True)
            flash("Welcome back, Administrator!", "success")
            return redirect(url_for("admin.dashboard"))

        db.session.add(AdminLoginAttempt(address_hash=address_hash))
        db.session.commit()
        flash("Invalid username or password.", "error")

    return render_template("admin/login.html", form=form)


@auth_bp.route("/admin-logout", methods=["POST"])
def admin_logout():
    if current_user.is_authenticated and current_user.is_admin:
        logout_user()
    session.clear()
    flash("Logged out from the admin panel.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    recent_questions = (
        Question.query.filter_by(status="approved")
        .order_by(Question.created_at.desc()).limit(3).all()
    )
    popular_playlists = Playlist.query.filter_by(status="approved").limit(3).all()
    total_questions = Question.query.filter_by(status="approved").count()
    total_students = User.query.filter_by(is_admin=False, profile_complete=True).count()

    return render_template(
        "index.html",
        recent_questions=recent_questions,
        popular_playlists=popular_playlists,
        total_questions=total_questions,
        total_students=total_students,
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    form = GuestLoginForm()
    if form.validate_on_submit():
        user = User(
            department=form.department.data,
            avatar=form.avatar.data,
            profile_complete=True,
            is_admin=False,
        )
        for attempt in range(3):
            try:
                user.anonymous_id = _guest_id_preview()
                user.name = user.anonymous_id
                db.session.add(user)
                db.session.commit()
                break
            except RuntimeError:
                flash("No anonymous IDs are available. Please contact the site administrator.", "error")
                return render_template("auth_login.html", form=form), 503
            except IntegrityError:
                db.session.rollback()
                session.pop("guest_id_preview", None)
                if attempt == 2:
                    current_app.logger.exception("Could not allocate a unique guest ID.")
                    flash("Could not create a guest profile. Please try again.", "error")
                    return render_template("auth_login.html", form=form), 503

        session.clear()
        session.permanent = True
        login_user(user, remember=False, fresh=True)
        flash(f"You're signed in as {user.anonymous_id}. Keep this ID to recognize your pseudonym.", "success")
        return redirect(url_for("dashboard.home"))

    try:
        anonymous_id_preview = _guest_id_preview()
    except RuntimeError:
        flash("No anonymous IDs are available. Please contact the site administrator.", "error")
        return render_template("auth_login.html", form=form), 503

    recent_questions = (
        Question.query.filter_by(status="approved")
        .order_by(Question.created_at.desc()).limit(3).all()
    )
    return render_template(
        "auth_login.html",
        form=form,
        recent_questions=recent_questions,
        anonymous_id_preview=anonymous_id_preview,
    )


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("auth.login"))
