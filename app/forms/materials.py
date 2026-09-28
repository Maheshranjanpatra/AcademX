from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, URL, ValidationError


def validate_file_size(form, field):
    """Custom validator to check file size (max 26MB)."""
    if field.data:
        file = field.data
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)
        if size > 10 * 1024 * 1024:
            raise ValidationError("File size must be less than 10MB.")


class MaterialUploadForm(FlaskForm):
    title = StringField(
        "Material Title",
        validators=[DataRequired(), Length(max=150)]
    )
    subject = StringField(
        "Course Code",
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
            FileAllowed(["pdf", "jpg", "jpeg", "docx"], "PDF, JPG, JPEG, or DOCX files only!"),
            validate_file_size
        ]
    )
    file_url = StringField(
        "External Resource Link (Optional)",
        validators=[Optional(), URL(), Length(max=500)]
    )
    submit = SubmitField("Upload Material")
