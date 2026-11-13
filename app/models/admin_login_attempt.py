from datetime import datetime, timezone
from app.extensions import db


def _utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class AdminLoginAttempt(db.Model):
    __tablename__ = "admin_login_attempts"

    id = db.Column(db.Integer, primary_key=True)
    address_hash = db.Column(db.String(64), nullable=False, index=True)
    attempted_at = db.Column(db.DateTime, nullable=False, default=_utcnow)
