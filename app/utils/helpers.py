import os
import cloudinary
import cloudinary.uploader
from flask import current_app
from werkzeug.utils import secure_filename
from app.utils.validators import YOUTUBE_ID_RE

def save_file(file_storage, subfolder):
    """Uploads a file to Cloudinary and returns the secure public URL.
    This ensures files persist across Render redeploys (which wipe local disk)."""
    cloudinary.config(
        cloud_name=current_app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=current_app.config['CLOUDINARY_API_KEY'],
        api_secret=current_app.config['CLOUDINARY_API_SECRET']
    )
    result = cloudinary.uploader.upload(
        file_storage,
        folder=f"nymora/{subfolder}",
        quality="auto:good",
        fetch_format="auto",
    )
    return result['secure_url']

def extract_youtube_id(value):
    """Extracts an 11-char YouTube ID from a raw ID or full URL. Returns None if not found."""
    if not value:
        return None
    match = YOUTUBE_ID_RE.search(value)
    return match.group(1) if match else None

def get_streak_animation(streak):
    """Maps a Streak object's state to the dashboard animation filename.
    Returns None if nothing should play this load."""
    if streak is None:
        return None
    if streak.egg_stage == "hatched":
        return "egg_hatch.mp4"
    elif streak.egg_stage == "cracking":
        return "egg_crack.mp4"
    elif streak.current_streak == 1:
        return "lay_egg.mp4"
    return None


def format_duration(seconds):
    if not seconds:
        return ""
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def youtube_thumbnail_url(youtube_id, quality="hqdefault"):
    if not youtube_id:
        return None
    return f"https://img.youtube.com/vi/{youtube_id}/{quality}.jpg"


def register_template_filters(app):
    app.jinja_env.filters["format_duration"] = format_duration
    app.jinja_env.filters["youtube_thumbnail"] = youtube_thumbnail_url

def get_progress_animation(done, total):
    """Maps playlist completion % to an animation filename (no extension)."""
    if total <= 0 or done <= 0:
        return None
    pct = (done / total) * 100
    if pct >= 100:
        return "egg_hatch"
    elif pct >= 67:
        return "egg_crack_02"
    elif pct >= 34:
        return "egg_crack_01"
    else:
        return "lay_egg"


def get_animation_copy(stage, done=None, total=None):
    """Title + message text for a given animation stage."""
    copy = {
        "lay_egg": ("A New Egg!", "You've started this playlist — your egg is laid."),
        "egg_crack_01": ("It's Cracking!", "Great progress — the egg is starting to crack."),
        "egg_crack_02": ("Almost There!", "The egg is cracking hard — you're close to hatching it."),
        "egg_hatch": ("Playlist Complete!", "Your egg hatched and flew away. Well done!"),
        "warning": ("A Snake is Circling...", "You missed yesterday. Complete a video today or your egg is gone."),
        "killed": ("Your Egg Was Lost", "The snake got to it. Your streak has reset — start a new egg today."),
    }
    title, message = copy.get(stage, ("", ""))
    if done is not None and total is not None and stage in ("lay_egg", "egg_crack_01", "egg_crack_02", "egg_hatch"):
        message += f" ({done}/{total} videos watched)"
    return title, message

