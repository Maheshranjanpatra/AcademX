import secrets
from datetime import datetime
from flask import url_for
from flask_login import UserMixin
from app.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(80))
    avatar = db.Column(db.String(100), default='avatar7.webp')

    profile_complete = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    questions = db.relationship(
        "Question",
        foreign_keys="Question.user_id",
        backref="author",
        lazy="dynamic",
    )
    answers = db.relationship("Answer", backref="author", lazy="dynamic")
    quiz_attempts = db.relationship("QuizAttempt", backref="user", lazy="dynamic")
    video_progress = db.relationship("VideoProgress", backref="user", lazy="dynamic")

    papers = db.relationship(
        "Paper",
        foreign_keys="Paper.uploaded_by",
        backref="uploader",
        lazy="dynamic",
    )
    reviewed_papers = db.relationship(
        "Paper",
        foreign_keys="Paper.reviewed_by",
        backref="reviewer",
        lazy="dynamic",
    )

    # ===== NEW: playlists uploaded by this user =====
    playlists_uploaded = db.relationship(
        "Playlist",
        foreign_keys="Playlist.uploaded_by",
        backref="uploader",
        lazy="dynamic",
    )

    anonymous_id = db.Column(db.String(20), unique=True)

    @property
    def username(self):
        return self.anonymous_id or ("admin" if self.is_admin else "guest")

    def generate_anonymous_id(self):
        """Assign an available pseudonymous ID from the four-digit namespace."""
        for number in secrets.SystemRandom().sample(range(10_000), 10_000):
            candidate = f"User_{number:04d}"
            existing = User.query.filter_by(anonymous_id=candidate).first()
            if existing is None or existing.id == self.id:
                self.anonymous_id = candidate
                self.name = candidate
                return candidate
        raise RuntimeError("All four-digit anonymous user IDs are in use.")

    @property
    def avatar_url(self):
        """Returns the URL to the user's avatar."""
        return url_for('static', filename=f'images/profiles/{self.avatar}')

    @property
    def is_active(self):
        return self.is_admin or self.profile_complete

    def __repr__(self):
        return f"<User {self.anonymous_id or 'admin'}>"
