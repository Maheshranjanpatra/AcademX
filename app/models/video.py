import re
from datetime import datetime
from app.extensions import db


class Playlist(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(80))
    description = db.Column(db.Text)

    videos = db.relationship(
        "Video",
        backref="playlist",
        lazy="select",
        order_by="Video.order_index",
        cascade="all, delete-orphan"
    )


class Video(db.Model):
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    youtube_video_id = db.Column(db.String(500), nullable=False)
    order_index = db.Column(db.Integer, default=0)
    duration_seconds = db.Column(db.Integer)

    progress_entries = db.relationship("VideoProgress", backref="video", lazy="dynamic")

    @property
    def youtube_url(self):
        """Return a properly formatted embed URL from any YouTube URL or ID."""
        url = self.youtube_video_id
        if not url:
            return None

        if '/embed/' in url or '/v/' in url:
            return url

        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[-1].split('?')[0]
            return f"https://www.youtube-nocookie.com/embed/{video_id}"

        if 'watch?v=' in url:
            video_id = url.split('watch?v=')[-1].split('&')[0]
            return f"https://www.youtube-nocookie.com/embed/{video_id}"

        if re.match(r'^[A-Za-z0-9_-]{11}$', url):
            return f"https://www.youtube-nocookie.com/embed/{url}"

        return url


class VideoProgress(db.Model):
    __tablename__ = "video_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey("videos.id"), nullable=False)

    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("user_id", "video_id", name="uq_user_video"),)
