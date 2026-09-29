from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, URL, ValidationError
from flask import current_app


def validate_file_size(form, field):
    """Check file size against MAX_CONTENT_LENGTH from config."""
    if field.data:
        file = field.data
        file.seek(0, 2)  
        size = file.tell()
        file.seek(0)  

        max_bytes = current_app.config["MAX_CONTENT_LENGTH"]
        max_mb = max_bytes // (1024 * 1024)

        if size > max_bytes:
            raise ValidationError(f"File size must be less than {max_mb}MB.")


class MaterialUploadForm(FlaskForm):
    title = StringField(
        "Material Title",
        validators=[DataRequired(), Length(max=150)]
    )
    subject = StringField(
        "Subject / Course Code",
        validators=[DataRequired(), Length(max=80)]
    )
    category = SelectField(
        "Category",
        choices=[
            ("Notes", "Lecture Notes"),
            ("Syllabus", "Syllabus"),
            ("Lab Manual", "Lab Manual"),
            ("Reference", "Reference"),
            ("Textbook","Textbook"),
            ("Other", "Other")
        ],
        validators=[DataRequired()]
    )
    description = TextAreaField(
        "Description",
        validators=[Optional(), Length(max=500)]
    )
    file = FileField(
        "Upload File (PDF / Image / Word)",
        validators=[
            FileAllowed(["pdf", "jpg", "jpeg", "png", "docx"], "PDF, JPG, PNG, or DOCX files only!"),
            validate_file_size
        ]
    )
    file_url = StringField(
        "External Resource Link (Optional)",
        validators=[Optional(), URL(), Length(max=500)]
    )
    submit = SubmitField("Upload Material")
