from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class UploadPaperForm(FlaskForm):
    subject = StringField(
        "Subject / Course Code",
        validators=[DataRequired(), Length(max=80)]
    )
    exam_type = SelectField(
        "Exam Type",
        choices=[
            ("internal", "Internal Exam"),
            ("semester", "Semester Exam")
        ],
        validators=[DataRequired()]
    )
    year = StringField(
        "Year (e.g. 2024)",
        validators=[DataRequired(), Length(max=10)]
    )
    file = FileField(
        "PDF Paper File",
        validators=[
            FileRequired(),
            FileAllowed(["pdf"], "PDF files only!")
        ]
    )
    submit = SubmitField("Upload Paper")
