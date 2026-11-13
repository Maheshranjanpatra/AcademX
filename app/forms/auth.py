from flask_wtf import FlaskForm
from wtforms import RadioField, SelectField
from wtforms.validators import DataRequired

VALID_DEPARTMENTS = {
    # ── School of Management ──
    "BKT": "Banking Technology",
    "ECO": "Economics",
    "IBU": "International Business",
    "MGT": "Management Studies",
    "MGK": "Management Studies (Karaikal)",
    "MGP": "Management Studies (Port Blair)",
    "TOU": "Tourism Studies",
    # ── Ramanujan School of Mathematical Sciences ──
    "MAT": "Mathematics",
    "STA": "Statistics",
    # ── Subramania Bharathi School of Tamil ──
    "TAM": "Tamil",
    # ── School of Physical, Chemical and Applied Sciences ──
    "PSY": "Applied Psychology",
    "CHE": "Chemistry",
    "CDM": "Coastal Disaster Management",
    "EAR": "Earth Sciences",
    "PHY": "Physics",
    # ── School of Life Sciences ──
    "BCM": "Biochemistry & Molecular Biology",
    "BIN": "Bioinformatics",
    "BTE": "Biotechnology",
    "EES": "Ecology & Environmental Sciences",
    "FST": "Food Science & Technology",
    "MIC": "Microbiology",
    "OMB": "Ocean Studies & Marine Biology (Port Blair)",
    # ── School of Humanities ──
    "CFL": "Foreign Languages",
    "ENG": "English",
    "FRE": "French",
    "HIN": "Hindi",
    "PHI": "Philosophy",
    "PED": "Physical Education & Sports",
    "ACS": "Asian Christian Studies",
    # ── School of Social Sciences and International Studies ──
    "CES": "European Studies",
    "CMS": "Maritime Studies",
    "CSI": "Study of Social Inclusion",
    "ANT": "Anthropology",
    "HIS": "History",
    "POL": "Politics & International Studies",
    "SWK": "Social Work",
    "SAS": "South Asian Studies",
    # ── School of Engineering and Technology ──
    "CPE": "Pollution Control & Environmental Engineering",
    "CSE": "Computer Science",
    "CSK": "Computer Science (Karaikal)",
    "ECE": "Electronics Engineering",
    # ── School of Education ──
    "ACE": "Adult & Continuing Education",
    "EDU": "Education",
    # ── School of Performing Arts ──
    "PFA": "Performing Arts",
    # ── School of Law ──
    "LAW": "Law",
    # ── School of Media and Communication ──
    "EMC": "Electronic Media & Mass Communication",
    "LIS": "Library & Information Science",
    # ── Madanjeet School of Green Energy Technologies ──
    "NST": "Nano Sciences & Technology",
    "GET": "Green Energy Technology",
    # ── LEGACY (backward compatibility only) ──
    "ITP": "ITEP [legacy]",
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
