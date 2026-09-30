from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class UserPlaylistForm(FlaskForm):
    title = StringField(
        "Playlist Title",
        validators=[DataRequired(), Length(max=150)]
    )
    subject = StringField(
        "Subject",
        validators=[Optional(), Length(max=80)]
    )
    description = TextAreaField(
        "Description",
        validators=[Optional(), Length(max=1000)]
    )
    video_urls = TextAreaField(
        "YouTube Video URLs (one per line)",
        validators=[DataRequired()],
        description="Paste one YouTube URL per line — watch, youtu.be, embed, or shorts links all work."
    )
    submit = SubmitField("Submit Playlist")
