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
    playlist_url = StringField(
        "YouTube Playlist URL",
        validators=[DataRequired(), Length(max=500)],
        description="Paste a full YouTube playlist link (must contain 'list=...')."
    )
    submit = SubmitField("Submit Playlist")
