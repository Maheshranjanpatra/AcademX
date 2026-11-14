from datetime import datetime
from flask import (
    Blueprint, render_template, redirect, url_for, abort, flash
)
from flask_login import login_required, current_user
from app.extensions import db
from app.models.video import Playlist, Video
from app.forms.video import UserPlaylistForm
from app.utils.youtube import (
    extract_playlist_id, extract_video_id, get_playlist_videos
)
from app.utils.telegram import notify_upload

video_bp = Blueprint("video", __name__)


def _uploader_display(user):
    for attr in ("username", "name", "full_name", "email"):
        v = getattr(user, attr, None)
        if v:
            return str(v)
    return f"User#{getattr(user, 'id', '?')}"


# PUBLIC: LIST PLAYLISTS (only approved)
@video_bp.route("/")
def playlists():
    all_playlists = (
        Playlist.query
        .filter_by(status="approved")
        .order_by(Playlist.created_at.desc())
        .all()
    )
    return render_template("video_playlists.html", playlists=all_playlists)


# USER: UPLOAD A PLAYLIST (goes to pending)
@video_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_playlist():
    form = UserPlaylistForm()

    if form.validate_on_submit():
        raw_url = (form.playlist_url.data or "").strip()

        playlist_id = extract_playlist_id(raw_url)
        if not playlist_id:
            if extract_video_id(raw_url):
                flash(
                    "That's a single video link, not a playlist. "
                    "Please paste a YouTube playlist URL (it contains 'list=...').",
                    "error"
                )
            else:
                flash(
                    "Invalid YouTube playlist URL. Please check and try again.",
                    "error"
                )
            return render_template("video_upload.html", form=form)

        try:
            videos_data = get_playlist_videos(playlist_id)
        except ValueError as e:
            flash(str(e), "error")
            return render_template("video_upload.html", form=form)
        except Exception:
            flash("Could not fetch this playlist from YouTube. Please try again.", "error")
            return render_template("video_upload.html", form=form)

        if not videos_data:
            flash(
                "No videos found in this playlist. Make sure it's public and not empty.",
                "error"
            )
            return render_template("video_upload.html", form=form)

        playlist = Playlist(
            title=form.title.data.strip(),
            subject=(form.subject.data or "").strip() or None,
            description=(form.description.data or "").strip() or None,
            uploaded_by=current_user.id,
            status="pending",
        )
        db.session.add(playlist)
        db.session.flush()

        for idx, v in enumerate(videos_data, start=1):
            video = Video(
                playlist_id=playlist.id,
                title=v["title"],
                youtube_video_id=v["video_id"],
                order_index=idx,
                duration_seconds=v["duration_seconds"],
            )
            db.session.add(video)

        db.session.commit()
        notify_upload(
            uploader=_uploader_display(current_user),
            item_type="YouTube Playlist",
            title=playlist.title or "(untitled)",
            link=url_for("admin.playlists", tab="pending", _external=True),
        )
        flash(
            f"Playlist submitted with {len(videos_data)} video(s) - "
            f"pending admin approval.",
            "success"
        )
        return redirect(url_for("materials.my_uploads"))

    return render_template("video_upload.html", form=form)


# WATCH (completion is tracked in the browser only)
@video_bp.route("/watch/<int:video_id>")
@login_required
def watch(video_id):
    video = Video.query.get_or_404(video_id)
    playlist = video.playlist

    if playlist.status != "approved":
        is_owner = (playlist.uploaded_by == current_user.id)
        if not (is_owner or current_user.is_admin):
            abort(404)

    return render_template("video_watch.html", video=video, playlist=playlist)
