from flask import Blueprint, redirect, url_for, render_template, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db, oauth
from app.models.user import User
from app.models.question import Question
from app.models.video import Playlist
from app.forms.auth import CompleteProfileForm
from app.forms.admin_login import AdminLoginForm  # NEW
import os

auth_bp = Blueprint("auth", __name__)

# ADMIN LOGIN (NEW ROUTES)

@auth_bp.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    """Admin login page with username/password from .env."""

    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.dashboard'))

    form = AdminLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')

        if username == admin_username and password == admin_password:
            admin_user = User.query.filter_by(is_admin=True).first()
            if not admin_user:
                admin_user = User(
                    google_sub='admin',
                    name='Administrator',
                    email='admin@academx.com',
                    is_admin=True,
                    profile_complete=True,
                    avatar='avatar1.png',
                    anonymous_id='User_0000'
                )
                db.session.add(admin_user)
                db.session.commit()

            login_user(admin_user, remember=False)
            flash('Welcome back, Administrator!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('admin/login.html', form=form)

@auth_bp.route("/admin-logout")
def admin_logout():
    """Logout from admin panel."""
    logout_user()
    flash('Logged out from admin panel.', 'success')
    return redirect(url_for('auth.login'))

# EXISTING ROUTES (unchanged)

@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    recent_questions = Question.query.order_by(Question.created_at.desc()).limit(3).all()
    popular_playlists = Playlist.query.limit(3).all()
    total_questions = Question.query.count()
    total_students = User.query.filter_by(profile_complete=True).count()

    return render_template(
        "index.html",
        recent_questions=recent_questions,
        popular_playlists=popular_playlists,
        total_questions=total_questions,
        total_students=total_students,
    )

@auth_bp.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    recent_questions = Question.query.order_by(Question.created_at.desc()).limit(3).all()
    return render_template("auth_login.html", recent_questions=recent_questions)

@auth_bp.route("/login/google")
def login_google():
    redirect_uri = url_for("auth.callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route("/callback")
def callback():
    try:
        token = oauth.google.authorize_access_token()
    except Exception as e:
        flash(f"Google authentication failed: {str(e)}", "error")
        return redirect(url_for("auth.login"))

    user_info = token.get("userinfo")

    if not user_info:
        flash("Could not retrieve your profile information.", "error")
        return redirect(url_for("auth.login"))

    email = user_info["email"]

    # @pondiuni.ac.in
    # if not email.endswith('@pondiuni.ac.in'):
    #     flash("Only @pondiuni.ac.in email addresses are allowed to sign in.", "error")
    #     return redirect(url_for("auth.login"))

    google_sub = user_info["sub"]
    name = user_info["name"]

    user = User.query.filter_by(google_sub=google_sub).first()

    if not user:
        user = User(google_sub=google_sub, email=email, name=name, profile_complete=False)
        user.generate_anonymous_id()
        db.session.add(user)
        db.session.commit()

    login_user(user, remember=True)

    if not user.profile_complete:
        return redirect(url_for("auth.complete_profile"))

    return redirect(url_for("dashboard.home"))

@auth_bp.route("/complete-profile", methods=["GET", "POST"])
@login_required
def complete_profile():
    if current_user.profile_complete:
        return redirect(url_for("dashboard.home"))

    form = CompleteProfileForm()

    if form.validate_on_submit():
        reg_num = current_user.email.split('@')[0]

        existing_user = User.query.filter(
            db.func.lower(User.reg_num) == db.func.lower(reg_num)
        ).first()
        if existing_user and existing_user.id != current_user.id:
            flash('This registration number is already registered. Please contact support.', 'error')
            return render_template("auth_complete_profile.html", form=form)

        current_user.department = form.department.data
        current_user.reg_num = reg_num
        current_user.avatar = form.avatar.data
        current_user.profile_complete = True

        if not current_user.anonymous_id:
            current_user.generate_anonymous_id()

        db.session.commit()

        flash('Profile completed successfully! Welcome to AcademX.', 'success')
        return redirect(url_for("dashboard.home"))

    return render_template("auth_complete_profile.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
