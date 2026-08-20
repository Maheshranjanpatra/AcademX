from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from app.models.question import Question
from app.models.video import Playlist, VideoProgress
from app.models.streak import Streak
from app.utils.decorators import profile_required
from app.utils.helpers import get_animation_copy

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
@profile_required
def home():
    recent_questions = Question.query.order_by(Question.created_at.desc()).limit(5).all()

    total_answers = current_user.answers.count()
    total_questions = current_user.questions.count()
    videos_completed = current_user.video_progress.filter_by(completed=True).count()

    playlists = Playlist.query.all()
    playlist_progress = []
    for pl in playlists:
        total = len(pl.videos)
        if total == 0:
            continue
        done = VideoProgress.query.join(VideoProgress.video).filter(
            VideoProgress.user_id == current_user.id,
            VideoProgress.completed == True,
        ).filter_by(playlist_id=pl.id).count()
        if done > 0:
            playlist_progress.append({"playlist": pl, "done": done, "total": total})

    grieving = False
    streak = Streak.query.filter_by(user_id=current_user.id).first()
    if streak:
        status = streak.check_daily_status()
        if status == "killed":
            title, message = get_animation_copy(status)
            session["animation_video"] = "kill_egg"
            session["animation_title"] = title
            session["animation_message"] = message
        elif status == "grieving":
            grieving = True

    return render_template(
        "dashboard.html",
        recent_questions=recent_questions,
        total_answers=total_answers,
        total_questions=total_questions,
        videos_completed=videos_completed,
        playlist_progress=playlist_progress,
        grieving=grieving,
    )
