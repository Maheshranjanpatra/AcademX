from datetime import datetime
from app.extensions import db

question_tags = db.Table(
    "question_tags",
    db.Column("question_id", db.Integer, db.ForeignKey("questions.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    is_anonymous = db.Column(db.Boolean, default=True)

    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    math_content = db.Column(db.Text)

    subject = db.Column(db.String(80))
    is_resolved = db.Column(db.Boolean, default=False)
    upvotes = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tags = db.relationship("Tag", secondary=question_tags, backref="questions")
    answers = db.relationship(
        "Answer", backref="question", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Question {self.id}: {self.title[:30]}>"


class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    is_anonymous = db.Column(db.Boolean, default=True)
    body = db.Column(db.Text, nullable=False)
    math_content = db.Column(db.Text)

    upvotes = db.Column(db.Integer, default=0)
    is_best_answer = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Answer {self.id} for Question {self.question_id}>"
