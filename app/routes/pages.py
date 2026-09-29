from flask import Blueprint, render_template
from flask import send_from_directory, current_app
from flask_login import login_required, current_user

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/about")
def about():
    return render_template("about.html")


@pages_bp.route("/contact")
def contact():
    return render_template("contact.html")


@pages_bp.route("/policy")
def policy():
    return render_template("policy.html")


@pages_bp.route("/offline")
def offline():
    return render_template("offline.html")


@pages_bp.route("/profile")
@login_required
def profile():
    """Full profile page — stats, progress, account info."""
    from app.models import Playlist, Video, VideoProgress
    from app.extensions import db

    playlists = Playlist.query.all()
    playlist_progress = []
    for pl in playlists:
        total = Video.query.filter_by(playlist_id=pl.id).count()
        completed = db.session.query(VideoProgress).join(Video).filter(
            Video.playlist_id == pl.id,
            VideoProgress.user_id == current_user.id,
            VideoProgress.completed == True
        ).count()
        if total > 0:
            playlist_progress.append({
                'title': pl.title,
                'subject': pl.subject,
                'total': total,
                'completed': completed,
                'percent': round((completed / total) * 100, 1)
            })

    questions_asked = current_user.questions.count()
    answers_given = current_user.answers.count()
    quizzes_taken = current_user.quiz_attempts.count()

    return render_template(
        "profile.html",
        playlist_progress=playlist_progress,
        questions_asked=questions_asked,
        answers_given=answers_given,
        quizzes_taken=quizzes_taken,
    )


@pages_bp.route("/sw.js")
def service_worker():
    return send_from_directory(current_app.static_folder, "sw.js", mimetype="application/javascript")