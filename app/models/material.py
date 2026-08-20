from datetime import datetime
from app.extensions import db


class Material(db.Model):
    __tablename__ = "materials"

    id = db.Column(db.Integer, primary_key=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    material_type = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50))
    file_path = db.Column(db.String(255))
    file_url = db.Column(db.String(255))
    subject = db.Column(db.String(80))

    status = db.Column(db.String(20), default="pending")
    reviewed_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    reviewed_at = db.Column(db.DateTime)

    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
