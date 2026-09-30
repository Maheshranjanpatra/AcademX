import random
from datetime import datetime
from flask import url_for
from flask_login import UserMixin
from app.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    google_sub = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    department = db.Column(db.String(80))
    reg_num = db.Column(db.String(40), unique=True)

    avatar = db.Column(db.String(100), default='avatar7.png')

    profile_complete = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    questions = db.relationship("Question", backref="author", lazy="dynamic")
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

    anonymous_id = db.Column(db.String(20), unique=True, nullable=False, default='')

    @property
    def username(self):
        """Returns the part of email before @ — used as display username."""
        return self.email.split('@')[0] if self.email else 'user'

    def generate_anonymous_id(self):
        """Generate a unique anonymous ID."""
        while True:
            new_id = f"User_{random.randint(1111, 9999)}"
            if not User.query.filter_by(anonymous_id=new_id).first():
                self.anonymous_id = new_id
                return new_id

    @property
    def avatar_url(self):
        """Returns the URL to the user's avatar."""
        return url_for('static', filename=f'images/profiles/{self.avatar}')

    def __repr__(self):
        return f"<User {self.email}>"
