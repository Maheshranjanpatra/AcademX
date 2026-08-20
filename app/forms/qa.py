from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Optional
from app.utils.constants import SUBJECT_CHOICES


class AskQuestionForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=200)]
    )
    body = TextAreaField(
        "Question",
        validators=[DataRequired()]
    )
    subject = SelectField(
        "Subject",
        choices=SUBJECT_CHOICES,
        validators=[DataRequired()]
    )
    tags = StringField(
        "Tags (comma-separated)",
        validators=[Optional()]
    )
    is_anonymous = BooleanField("Post anonymously", default=True)


class AnswerForm(FlaskForm):
    body = TextAreaField(
        "Your Answer",
        validators=[DataRequired()]
    )
    is_anonymous = BooleanField("Answer anonymously", default=True)
