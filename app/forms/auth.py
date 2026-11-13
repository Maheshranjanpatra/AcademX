from flask_wtf import FlaskForm
from wtforms import RadioField, SelectField
from wtforms.validators import DataRequired

VALID_DEPARTMENTS = {
    'MAT': 'Mathematics',
    'PHY': 'Physics',
    'CHE': 'Chemistry',
    'HIS': 'History',
    'ITP': 'ITEP',
    'CSE': 'Computer Science',
    'BIO': 'Biology',
    'ECO': 'Economics',
    'ENG': 'English',
    'STA': 'Statistics',
}


class GuestLoginForm(FlaskForm):
    department = SelectField(
        "Department",
        choices=[('', 'Select your department')]
        + [(code, name) for code, name in VALID_DEPARTMENTS.items()],
        validators=[DataRequired()],
    )

    avatar = RadioField(
        "Choose Profile Picture",
        choices=[(f"avatar{number}.webp", f"Avatar {number}") for number in range(1, 11)],
        default='avatar7.webp',
        validators=[DataRequired()],
    )
