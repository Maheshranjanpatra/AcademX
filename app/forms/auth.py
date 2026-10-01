from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
import re



# VALID LISTS (You can expand these)

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
"""
VALID_DEGREES = {
    'BS': 'B.Sc (Hons)',
    'MS': 'M.Sc',
    'BA': 'B.A',
    'MA': 'M.A',
    'BCOM': 'B.Com',
    'MCOM': 'M.Com',
    'BBA': 'B.B.A',
    'MBA': 'M.B.A',
    'BED': 'B.Ed',
    'MED': 'M.Ed',
}

VALID_LOCATIONS = {
    'PY': 'Puducherry',
}

# CUSTOM VALIDATOR

def validate_reg_num(form, field):

    reg_num = field.data.strip().upper()  # Convert to uppercase

    if len(reg_num) != 13:
        raise ValidationError('Registration number must be exactly 13 characters.')

    pattern = r'^(\d{2})([A-Z]{2})([A-Z]{3})([A-Z]{2})(\d{4})$'
    match = re.match(pattern, reg_num)

    if not match:
        raise ValidationError(
            'Invalid format. Expected: 25BSMATPY0011 (2-digit year + 2-letter degree + 3-letter dept + 2-letter location + 4-digit serial)'
        )

    year, degree, dept, location, serial = match.groups()

    year_num = int(year)
    if year_num < 21 or year_num > 26:
        raise ValidationError(f'Invalid year. Expected: 20-29 (for 2020-2029), got: {year}')

    if degree not in VALID_DEGREES:
        raise ValidationError(
            f'Invalid degree code: {degree}. Valid options: {", ".join(VALID_DEGREES.keys())}'
        )

    if dept not in VALID_DEPARTMENTS:
        raise ValidationError(
            f'Invalid department code: {dept}. Valid options: {", ".join(VALID_DEPARTMENTS.keys())}'
        )

    if location not in VALID_LOCATIONS:
        raise ValidationError(
            f'Invalid location code: {location}. Valid options: {", ".join(VALID_LOCATIONS.keys())}'
        )

    if serial == '0000':
        raise ValidationError('Serial number cannot be 0000.')
"""


# FORM


class CompleteProfileForm(FlaskForm):
    department = SelectField(
        "Department",
        choices=[
            ('', 'Select your department'),
        ] + [(code, name) for code, name in VALID_DEPARTMENTS.items()],
        validators=[DataRequired()]
    )

    """
    reg_num = StringField(
        "Registration Number",
        validators=[
            DataRequired(),
            Length(min=13, max=13, message='Registration number must be exactly 13 characters.'),
            validate_reg_num
        ]
    )
    """

    avatar = RadioField(
        "Choose Profile Picture",
        choices=[
            ('avatar1.webp', 'Avatar 1'),
            ('avatar2.webp', 'Avatar 2'),
            ('avatar3.webp', 'Avatar 3'),
            ('avatar4.webp', 'Avatar 4'),
            ('avatar5.webp', 'Avatar 5'),
            ('avatar6.webp', 'Avatar 6'),
            ('avatar7.webp', 'Avatar 7'),
            ('avatar8.webp', 'Avatar 8'),
            ('avatar9.webp', 'Avatar 9'),
            ('avatar10.webp', 'Avatar 10'),
        ],
        default='avatar7.webp',
        validators=[DataRequired()]
    )
