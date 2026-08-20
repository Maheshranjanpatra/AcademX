from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional


class QuizForm(FlaskForm):
    """Used when an admin/teacher creates a new quiz shell (topic or PYQ)."""

    title = StringField(
        "Title", validators=[DataRequired(), Length(max=150)]
    )
    subject = StringField(
        "Subject", validators=[DataRequired(), Length(max=80)]
    )
    quiz_type = SelectField(
        "Quiz Type",
        choices=[("topic", "Topic-wise"), ("pyq", "Previous Year Questions")],
        default="topic",
        validators=[DataRequired()],
    )
    description = TextAreaField(
        "Description", validators=[Optional(), Length(max=1000)]
    )


class QuizQuestionForm(FlaskForm):
    """Used to add a single MCQ question to an existing quiz."""

    question_text = TextAreaField(
        "Question", validators=[DataRequired(), Length(max=2000)]
    )
    option_a = StringField(
        "Option A", validators=[DataRequired(), Length(max=255)]
    )
    option_b = StringField(
        "Option B", validators=[DataRequired(), Length(max=255)]
    )
    option_c = StringField(
        "Option C", validators=[DataRequired(), Length(max=255)]
    )
    option_d = StringField(
        "Option D", validators=[DataRequired(), Length(max=255)]
    )
    correct_option = SelectField(
        "Correct Option",
        choices=[("a", "A"), ("b", "B"), ("c", "C"), ("d", "D")],
        validators=[DataRequired()],
    )
    explanation = TextAreaField(
        "Explanation", validators=[Optional(), Length(max=1000)]
    )
