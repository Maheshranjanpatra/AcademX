import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, session, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.video import Playlist, Video, VideoProgress
from app.models.streak import Streak
from app.utils.decorators import profile_required
from app.utils.helpers import get_progress_animation, get_animation_copy

video_bp = Blueprint("video", __name__)

def _set_progress_animation(user_id, video):
    """Shared logic: after marking a video complete, checks this
    playlist's completion % and queues the matching animation."""
    playlist = video.playlist
    total = len(playlist.videos)
    done = VideoProgress.query.join(VideoProgress.video).filter(
        VideoProgress.user_id == user_id,
        VideoProgress.completed == True,
    ).filter_by(playlist_id=playlist.id).count()

    stage = get_progress_animation(done, total)
    if stage:
        title, message = get_animation_copy(stage, done, total)
        session["animation_video"] = stage
        session["animation_title"] = title
        session["animation_message"] = message

@video_bp.route("/")
def playlists():
    all_playlists = Playlist.query.all()
    return render_template("video_playlists.html", playlists=all_playlists)

@video_bp.route("/watch/<int:video_id>")
@login_required
@profile_required
def watch(video_id):
    video = Video.query.get_or_404(video_id)
    playlist = video.playlist

    user_progress = VideoProgress.query.filter_by(
        user_id=current_user.id, video_id=video.id
    ).first()
    is_completed = user_progress.completed if user_progress else False

    completed_video_ids = set(
        vp.video_id for vp in VideoProgress.query.filter_by(
            user_id=current_user.id, completed=True
        ).all()
    )

    return render_template(
        "video_watch.html",
        video=video,
        playlist=playlist,
        is_completed=is_completed,
        completed_video_ids=completed_video_ids
    )

@video_bp.route("/<int:video_id>/complete", methods=["POST"])
@login_required
@profile_required
def mark_complete(video_id):
    progress = VideoProgress.query.filter_by(
        user_id=current_user.id, video_id=video_id
    ).first()

    if not progress:
        progress = VideoProgress(user_id=current_user.id, video_id=video_id)
        db.session.add(progress)

    progress.completed = True
    progress.completed_at = datetime.utcnow()

    """
    # Update daily study streak
    streak = Streak.query.filter_by(user_id=current_user.id).first()
    if not streak:
        streak = Streak(user_id=current_user.id)
        db.session.add(streak)
    streak_changed = streak.register_completion()
    db.session.commit()
    if streak_changed:
        session["show_streak_animation"] = True
        session["egg_stage"] = streak.egg_stage
        session["current_streak"] = streak.current_streak
    """
    db.session.commit()

    session["show_completion_modal"] = True
    session["completion_video_id"] = video_id
    session["completion_video_title"] = Video.query.get(video_id).title

    return redirect(url_for("video.watch", video_id=video_id))

"""
@video_bp.route("/clear-streak-animation", methods=["POST"])
def clear_streak_animation():
    for key in ("animation_video", "animation_title", "animation_message",
                "show_streak_animation", "egg_stage", "current_streak"):
        session.pop(key, None)
    return '', 204
"""

@video_bp.route("/clear-completion-modal", methods=["POST"])
def clear_completion_modal():
    session.pop("show_completion_modal", None)
    session.pop("completion_video_id", None)
    session.pop("completion_video_title", None)
    return "", 204

@video_bp.route("/<int:video_id>/toggle-complete", methods=["POST"])
@login_required
@profile_required
def toggle_complete(video_id):
    progress = VideoProgress.query.filter_by(
        user_id=current_user.id, video_id=video_id
    ).first()
    video = Video.query.get(video_id)

    if not progress:
        progress = VideoProgress(user_id=current_user.id, video_id=video_id)
        progress.completed = True
        progress.completed_at = datetime.utcnow()
        db.session.add(progress)

        streak = Streak.query.filter_by(user_id=current_user.id).first()
        if not streak:
            streak = Streak(user_id=current_user.id)
            db.session.add(streak)
        streak.register_completion()
        db.session.commit()

        _set_progress_animation(current_user.id, video)
    else:
        progress.completed = not progress.completed
        if progress.completed:
            progress.completed_at = datetime.utcnow()
            streak = Streak.query.filter_by(user_id=current_user.id).first()
            if not streak:
                streak = Streak(user_id=current_user.id)
                db.session.add(streak)
            streak.register_completion()
            db.session.commit()

            _set_progress_animation(current_user.id, video)
        else:
            db.session.commit()

    session["show_completion_modal"] = True
    session["completion_video_id"] = video_id
    session["completion_video_title"] = video.title

    print(f"✅ Modal set for video: {video.title}")

    return redirect(url_for("video.watch", video_id=video_id))
