import re
from wtforms.validators import ValidationError

YOUTUBE_ID_RE = re.compile(
    r"(?:v=|\/embed\/|youtu\.be\/|\/v\/|\/e\/|watch\?v=|^)([0-9A-Za-z_-]{11})"
)
ACADEMIC_YEAR_RE = re.compile(r"^\d{4}-\d{2}$")


class ValidYouTubeInput:
    def __init__(self, message=None):
        self.message = message or "Enter a valid YouTube video ID or URL."

    def __call__(self, form, field):
        if not field.data:
            return
        if not YOUTUBE_ID_RE.search(field.data):
            raise ValidationError(self.message)


class ValidAcademicYear:
    def __init__(self, message=None):
        self.message = message or "Use the format YYYY-YY, e.g. 2024-25."

    def __call__(self, form, field):
        if not field.data:
            return
        if not ACADEMIC_YEAR_RE.match(field.data):
            raise ValidationError(self.message)


def validate_youtube_url(value):
    """Plain boolean check (not tied to a WTForms field) — usable in routes
    or scripts, e.g. before calling extract_youtube_id()."""
    if not value:
        return False
    return bool(YOUTUBE_ID_RE.search(value))


def allowed_file(filename, allowed_extensions):
    """Checks a filename's extension against an allowed set, e.g.
    allowed_file(file.filename, {"pdf", "jpg", "png"})."""
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in allowed_extensions
