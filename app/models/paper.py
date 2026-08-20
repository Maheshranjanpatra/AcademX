from datetime import datetime
from app.extensions import db


class Paper(db.Model):
    """Previous-year question papers / internals, uploaded by students,
    gated behind admin approval before becoming public."""
    __tablename__ = "papers"

    id = db.Column(db.Integer, primary_key=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    subject = db.Column(db.String(80), nullable=False)
    exam_type = db.Column(db.String(20))
    year = db.Column(db.String(9))
    file_path = db.Column(db.String(255), nullable=False)

    status = db.Column(db.String(20), default="pending")
    reviewed_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    reviewed_at = db.Column(db.DateTime)

    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
