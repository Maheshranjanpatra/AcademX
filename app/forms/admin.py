from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, URL


class QuizAdminForm(FlaskForm):
    title = StringField(
        "Quiz Title",
        validators=[DataRequired(), Length(max=150)]
    )
    subject = StringField(
        "Subject",
        validators=[DataRequired(), Length(max=80)]
    )
    quiz_type = SelectField(
        "Quiz Type",
        choices=[
            ("practice", "Practice"),
            ("pyq", "PYQ Practice"),
            ("topic", "Topic Specific")
        ],
        validators=[DataRequired()]
    )
    description = TextAreaField(
        "Description",
        validators=[Optional(), Length(max=500)]
    )
    submit = SubmitField("Save Quiz")


class QuestionAdminForm(FlaskForm):
    question_text = TextAreaField(
        "Question Text",
        validators=[DataRequired()]
    )
    option_a = StringField("Option A", validators=[DataRequired(), Length(max=255)])
    option_b = StringField("Option B", validators=[DataRequired(), Length(max=255)])
    option_c = StringField("Option C", validators=[DataRequired(), Length(max=255)])
    option_d = StringField("Option D", validators=[DataRequired(), Length(max=255)])
    correct_option = SelectField(
        "Correct Answer Option",
        choices=[("a", "Option A"), ("b", "Option B"), ("c", "Option C"), ("d", "Option D")],
        validators=[DataRequired()]
    )
    explanation = TextAreaField(
        "Explanation / Solution",
        validators=[Optional()]
    )
    submit = SubmitField("Save Question")


class PlaylistAdminForm(FlaskForm):
    title = StringField(
        "Playlist Title",
        validators=[DataRequired(), Length(max=150)]
    )
    subject = StringField(
        "Subject / Course Code",
        validators=[DataRequired(), Length(max=80)]
    )
    description = TextAreaField(
        "Description",
        validators=[Optional(), Length(max=500)]
    )
    submit = SubmitField("Save Playlist")


class VideoAdminForm(FlaskForm):
    title = StringField(
        "Video Title",
        validators=[DataRequired(), Length(max=200)]
    )
    youtube_url = StringField(
        "YouTube Embed URL",
        validators=[DataRequired(), Length(max=500), URL()]
    )
    order_index = IntegerField(
        "Order Index (Sequence)",
        default=1,
        validators=[DataRequired(), NumberRange(min=1)]
    )
    duration_seconds = IntegerField(
        "Duration (Seconds)",
        validators=[Optional(), NumberRange(min=0)]
    )
    submit = SubmitField("Save Video")
