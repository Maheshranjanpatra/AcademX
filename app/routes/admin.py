from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import current_user
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from app.extensions import db
from app.models.user import User
from app.models.question import Question, Answer
from app.models.paper import Paper
from app.models.quiz import Quiz, QuizQuestion, QuizAttempt
from app.models.video import Playlist, Video, VideoProgress
from app.models.material import Material
from app.models.streak import Streak
from app.utils.decorators import admin_required, check_session_timeout
from app.utils.youtube import get_playlist_videos, get_playlist_details, extract_playlist_id
from app.utils.helpers import save_file
from app.forms.admin import QuizAdminForm, QuestionAdminForm, PlaylistAdminForm, VideoAdminForm
from app.forms.materials import MaterialUploadForm


# BLUEPRINT DEFINITION
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.context_processor
def inject_admin_globals():
    return {
        'sidebar_pending_papers':    Paper.query.filter_by(status='pending').count(),
        'sidebar_pending_playlists': Playlist.query.filter_by(status='pending').count(),
        'sidebar_pending_questions': Question.query.filter_by(status='pending').count(),
        'sidebar_pending_materials': Material.query.filter_by(status='pending').count(),
    }

# DASHBOARD

@admin_bp.route("/")
@admin_required
@check_session_timeout
def dashboard():
    """Admin dashboard with metrics and charts."""

    total_users = User.query.filter_by(is_admin=False).count()
    total_questions = Question.query.count()
    pending_papers = Paper.query.filter_by(status="pending").count()
    pending_playlists = Playlist.query.filter_by(status="pending").count()
    total_quizzes = Quiz.query.count()

    one_week_ago = datetime.utcnow() - timedelta(days=7)

    users_last_week = User.query.filter(
        User.is_admin.is_(False), User.created_at >= one_week_ago
    ).count()
    questions_last_week = Question.query.filter(Question.created_at >= one_week_ago).count()
    quizzes_last_week = Quiz.query.filter(Quiz.created_at >= one_week_ago).count()

    daily_users = []
    day_labels = []
    for i in range(6, -1, -1):
        day = datetime.utcnow().date() - timedelta(days=i)
        count = User.query.filter(
            User.is_admin.is_(False), func.date(User.created_at) == day
        ).count()
        daily_users.append(count)
        day_labels.append(day.strftime('%a'))

    activities = []

    recent_questions = Question.query.order_by(Question.created_at.desc()).limit(5).all()
    for q in recent_questions:
        author = User.query.get(q.user_id)
        activities.append({
            'type': 'question',
            'user': author.anonymous_id if author else 'Unknown',
            'action': f'asked "{q.title[:50]}"',
            'time': q.created_at,
            'icon': 'forum',
            'color': 'var(--accent-primary)',
            'url': url_for('qa.view_question', question_id=q.id)
        })

    recent_papers = Paper.query.order_by(Paper.uploaded_at.desc()).limit(5).all()
    for p in recent_papers:
        uploader = User.query.get(p.uploaded_by)
        status_icon = 'check_circle' if p.status == 'approved' else 'schedule' if p.status == 'pending' else 'cancel'
        status_color = 'var(--accent-secondary)' if p.status == 'approved' else 'var(--accent-gold)' if p.status == 'pending' else 'var(--accent-danger)'
        activities.append({
            'type': 'paper',
            'user': uploader.anonymous_id if uploader else 'Unknown',
            'action': f'uploaded a paper: {p.subject} ({p.status})',
            'time': p.uploaded_at,
            'icon': status_icon,
            'color': status_color,
            'url': url_for('admin.papers')
        })

    activities = sorted(activities, key=lambda x: x['time'], reverse=True)[:10]

    metrics = {
        'users':             total_users,
        'users_trend':       f'+{users_last_week}' if users_last_week > 0 else f'{users_last_week}',
        'questions':         total_questions,
        'questions_trend':   f'+{questions_last_week}' if questions_last_week > 0 else f'{questions_last_week}',
        'papers':            pending_papers,
        'playlists':         pending_playlists,
        'quizzes':           total_quizzes,
        'quizzes_trend':     f'+{quizzes_last_week}' if quizzes_last_week > 0 else f'{quizzes_last_week}',
    }

    return render_template(
        'admin/dashboard.html',
        metrics=metrics,
        daily_users=daily_users,
        day_labels=day_labels,
        activities=activities
    )

# USER MANAGEMENT

@admin_bp.route("/users")
@admin_required
@check_session_timeout
def users():
    search = request.args.get('search', '')
    department = request.args.get('department', '')
    status = request.args.get('status', '')
    page = request.args.get('page', 1, type=int)
    per_page = 15

    query = User.query.filter_by(is_admin=False)

    if search:
        query = query.filter(
            db.or_(
                User.anonymous_id.ilike(f'%{search}%'),
                User.department.ilike(f'%{search}%')
            )
        )

    if department:
        query = query.filter_by(department=department)

    if status == 'active':
        query = query.filter_by(profile_complete=True)
    elif status == 'inactive':
        query = query.filter_by(profile_complete=False)

    departments = db.session.query(User.department).distinct().all()
    departments = [d[0] for d in departments if d[0]]

    paginated = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        'admin/users.html',
        users=paginated.items,
        pagination=paginated,
        departments=departments,
        search=search,
        department=department,
        status=status
    )

@admin_bp.route("/users/<int:user_id>")
@admin_required
@check_session_timeout
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        abort(404)

    stats = {
        'questions': user.questions.count(),
        'answers': user.answers.count(),
        'quiz_attempts': user.quiz_attempts.count(),
        'videos_completed': VideoProgress.query.filter_by(
            user_id=user.id, completed=True
        ).count(),
        'streak': Streak.query.filter_by(user_id=user.id).first()
    }

    return render_template('admin/user_detail.html', user=user, stats=stats)

@admin_bp.route("/users/<int:user_id>/toggle-status", methods=["POST"])
@admin_required
@check_session_timeout
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)

    if user.is_admin:
        flash("Admin account status cannot be changed here.", "error")
        return redirect(url_for('admin.users'))

    user.profile_complete = not user.profile_complete
    db.session.commit()

    status = "enabled" if user.profile_complete else "disabled"
    flash(f"{user.anonymous_id} has been {status}.", "success")
    return redirect(url_for('admin.users'))

@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@admin_required
@check_session_timeout
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.is_admin:
        flash("Admin accounts cannot be deleted here.", "error")
        return redirect(url_for('admin.users'))

    anonymous_id = user.anonymous_id
    Streak.query.filter_by(user_id=user_id).delete()
    VideoProgress.query.filter_by(user_id=user_id).delete()
    QuizAttempt.query.filter_by(user_id=user_id).delete()
    Answer.query.filter_by(user_id=user_id).delete()
    Question.query.filter_by(user_id=user_id).delete()
    Paper.query.filter_by(uploaded_by=user_id).delete()
    Material.query.filter_by(uploaded_by=user_id).delete()
    Playlist.query.filter_by(uploaded_by=user_id).update(
        {"uploaded_by": None}, synchronize_session=False
    )
    Quiz.query.filter_by(created_by=user_id).update(
        {"created_by": None}, synchronize_session=False
    )

    db.session.delete(user)
    db.session.commit()

    flash(f"{anonymous_id} has been permanently deleted.", "success")
    return redirect(url_for('admin.users'))

# PAPER MODERATION

@admin_bp.route("/papers")
@admin_required
@check_session_timeout
def papers():
    tab = request.args.get('tab', 'pending')
    search = request.args.get('search', '')

    query = Paper.query

    if tab == 'pending':
        query = query.filter_by(status='pending')
    elif tab == 'approved':
        query = query.filter_by(status='approved')
    elif tab == 'rejected':
        query = query.filter_by(status='rejected')

    if search:
        query = query.filter(
            db.or_(
                Paper.subject.ilike(f'%{search}%'),
                Paper.year.ilike(f'%{search}%')
            )
        )

    papers = query.order_by(Paper.uploaded_at.desc()).all()

    pending_count = Paper.query.filter_by(status='pending').count()
    approved_count = Paper.query.filter_by(status='approved').count()
    rejected_count = Paper.query.filter_by(status='rejected').count()

    return render_template(
        'admin/papers.html',
        papers=papers,
        tab=tab,
        pending_count=pending_count,
        approved_count=approved_count,
        rejected_count=rejected_count,
        search=search
    )

@admin_bp.route("/papers/<int:paper_id>/approve", methods=["POST"])
@admin_required
@check_session_timeout
def approve_paper(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    if paper.status != 'pending':
        flash("This paper has already been reviewed.", "warning")
        return redirect(url_for('admin.papers'))

    paper.status = 'approved'
    paper.reviewed_by = current_user.id
    paper.reviewed_at = datetime.utcnow()
    db.session.commit()
    flash(f"Paper '{paper.subject}' has been approved.", "success")
    return redirect(url_for('admin.papers'))

@admin_bp.route("/papers/<int:paper_id>/reject", methods=["POST"])
@admin_required
@check_session_timeout
def reject_paper(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    if paper.status != 'pending':
        flash("This paper has already been reviewed.", "warning")
        return redirect(url_for('admin.papers'))

    paper.status = 'rejected'
    paper.reviewed_by = current_user.id
    paper.reviewed_at = datetime.utcnow()
    db.session.commit()
    flash(f"Paper '{paper.subject}' has been rejected.", "success")
    return redirect(url_for('admin.papers'))

@admin_bp.route("/papers/<int:paper_id>/delete", methods=["POST"])
@admin_required
@check_session_timeout
def delete_paper(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    db.session.delete(paper)
    db.session.commit()
    flash(f"Paper '{paper.subject}' has been deleted.", "success")
    return redirect(url_for('admin.papers'))

@admin_bp.route("/papers/batch-action", methods=["POST"])
@admin_required
@check_session_timeout
def batch_paper_action():
    paper_ids = request.form.getlist('paper_ids')
    action = request.form.get('action')

    if not paper_ids:
        flash("No papers selected.", "warning")
        return redirect(url_for('admin.papers'))

    papers = Paper.query.filter(Paper.id.in_(paper_ids)).all()

    if action == 'approve':
        for paper in papers:
            if paper.status == 'pending':
                paper.status = 'approved'
                paper.reviewed_by = current_user.id
                paper.reviewed_at = datetime.utcnow()
        flash(f"{len(papers)} papers approved.", "success")
    elif action == 'reject':
        for paper in papers:
            if paper.status == 'pending':
                paper.status = 'rejected'
                paper.reviewed_by = current_user.id
                paper.reviewed_at = datetime.utcnow()
        flash(f"{len(papers)} papers rejected.", "success")
    elif action == 'delete':
        for paper in papers:
            db.session.delete(paper)
        flash(f"{len(papers)} papers deleted.", "success")

    db.session.commit()
    return redirect(url_for('admin.papers'))

# PLAYLIST MODERATION

@admin_bp.route("/playlists")
@admin_required
@check_session_timeout
def playlists():
    tab = request.args.get('tab', 'pending')
    search = request.args.get('search', '')

    query = Playlist.query

    if tab == 'pending':
        query = query.filter_by(status='pending')
    elif tab == 'approved':
        query = query.filter_by(status='approved')
    elif tab == 'rejected':
        query = query.filter_by(status='rejected')

    if search:
        query = query.filter(
            db.or_(
                Playlist.title.ilike(f'%{search}%'),
                Playlist.subject.ilike(f'%{search}%')
            )
        )

    playlists = query.order_by(Playlist.created_at.desc()).all()

    pending_count  = Playlist.query.filter_by(status='pending').count()
    approved_count = Playlist.query.filter_by(status='approved').count()
    rejected_count = Playlist.query.filter_by(status='rejected').count()

    return render_template(
        'admin/playlists.html',
        playlists=playlists,
        tab=tab,
        pending_count=pending_count,
        approved_count=approved_count,
        rejected_count=rejected_count,
        search=search
    )


@admin_bp.route("/playlists/<int:playlist_id>/approve", methods=["POST"])
@admin_required
@check_session_timeout
def approve_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.status != 'pending':
        flash("This playlist has already been reviewed.", "warning")
        return redirect(url_for('admin.playlists'))

    playlist.status = 'approved'
    db.session.commit()
    flash(f"Playlist '{playlist.title}' has been approved.", "success")
    return redirect(url_for('admin.playlists'))


@admin_bp.route("/playlists/<int:playlist_id>/reject", methods=["POST"])
@admin_required
@check_session_timeout
def reject_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.status != 'pending':
        flash("This playlist has already been reviewed.", "warning")
        return redirect(url_for('admin.playlists'))

    playlist.status = 'rejected'
    db.session.commit()
    flash(f"Playlist '{playlist.title}' has been rejected.", "success")
    return redirect(url_for('admin.playlists'))


@admin_bp.route("/playlists/<int:playlist_id>/delete", methods=["POST"])
@admin_required
@check_session_timeout
def delete_playlist_admin(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    title = playlist.title
    db.session.delete(playlist)
    db.session.commit()
    flash(f"Playlist '{title}' has been deleted.", "success")
    return redirect(url_for('admin.playlists'))

# Q&A MODERATION

@admin_bp.route("/qa")
@admin_required
@check_session_timeout
def qa():
    search = request.args.get('search', '')
    status = request.args.get('status', 'pending')

    query = Question.query
    if status in {'pending', 'approved', 'rejected'}:
        query = query.filter_by(status=status)

    if search:
        query = query.filter(
            db.or_(
                Question.title.ilike(f'%{search}%'),
                Question.body.ilike(f'%{search}%')
            )
        )

    if request.args.get('resolution') == 'resolved':
        query = query.filter_by(is_resolved=True)
    elif request.args.get('resolution') == 'unresolved':
        query = query.filter_by(is_resolved=False)

    questions = query.order_by(Question.created_at.desc()).all()

    return render_template(
        'admin/qa.html',
        questions=questions,
        search=search,
        status=status,
        pending_count=Question.query.filter_by(status='pending').count(),
        approved_count=Question.query.filter_by(status='approved').count(),
        rejected_count=Question.query.filter_by(status='rejected').count(),
    )

@admin_bp.route("/qa/<int:question_id>/approve", methods=["POST"])
@admin_required
@check_session_timeout
def approve_question(question_id):
    question = Question.query.get_or_404(question_id)
    if question.status != 'pending':
        flash("This question has already been reviewed.", "warning")
        return redirect(url_for('admin.qa', status='pending'))

    question.status = 'approved'
    question.reviewed_by = current_user.id
    question.reviewed_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.session.commit()
    flash("Question approved and published.", "success")
    return redirect(url_for('admin.qa', status='pending'))

@admin_bp.route("/qa/<int:question_id>/reject", methods=["POST"])
@admin_required
@check_session_timeout
def reject_question(question_id):
    question = Question.query.get_or_404(question_id)
    if question.status != 'pending':
        flash("This question has already been reviewed.", "warning")
        return redirect(url_for('admin.qa', status='pending'))

    question.status = 'rejected'
    question.reviewed_by = current_user.id
    question.reviewed_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.session.commit()
    flash("Question rejected.", "success")
    return redirect(url_for('admin.qa', status='pending'))

@admin_bp.route("/qa/<int:question_id>/delete", methods=["POST"])
@admin_required
@check_session_timeout
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash("Question has been deleted.", "success")
    return redirect(url_for('admin.qa'))

@admin_bp.route("/qa/<int:question_id>/toggle-resolved", methods=["POST"])
@admin_required
@check_session_timeout
def toggle_resolved(question_id):
    question = Question.query.get_or_404(question_id)
    question.is_resolved = not question.is_resolved
    db.session.commit()
    status = "resolved" if question.is_resolved else "unresolved"
    flash(f"Question marked as {status}.", "success")
    return redirect(url_for('admin.qa'))

@admin_bp.route("/qa/answer/<int:answer_id>/delete", methods=["POST"])
@admin_required
@check_session_timeout
def delete_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    db.session.delete(answer)
    db.session.commit()
    flash("Answer has been deleted.", "success")
    return redirect(url_for('admin.qa'))

# QUIZ MANAGEMENT

@admin_bp.route("/quizzes")
@admin_required
@check_session_timeout
def quizzes():
    search = request.args.get('search', '')
    subject = request.args.get('subject', '')

    query = Quiz.query

    if search:
        query = query.filter(Quiz.title.ilike(f'%{search}%'))
    if subject:
        query = query.filter_by(subject=subject)

    quizzes = query.order_by(Quiz.created_at.desc()).all()

    subjects = db.session.query(Quiz.subject).distinct().all()
    subjects = [s[0] for s in subjects if s[0]]

    return render_template('admin/quizzes.html', quizzes=quizzes, subjects=subjects, search=search, subject=subject)


@admin_bp.route("/quizzes/create", methods=["GET", "POST"])
@admin_required
@check_session_timeout
def create_quiz():
    form = QuizAdminForm()

    if form.validate_on_submit():
        quiz = Quiz(
            title=form.title.data,
            subject=form.subject.data,
            quiz_type=form.quiz_type.data,
            description=form.description.data,
            created_by=current_user.id
        )
        db.session.add(quiz)
        db.session.commit()
        flash(f"Quiz '{quiz.title}' has been created.", "success")
        return redirect(url_for('admin.quizzes'))

    if request.method == 'POST' and not form.validate():
        flash('Invalid form submission. Please check the errors below.', 'error')

    return render_template('admin/quiz_form.html', form=form, action='Create')

@admin_bp.route("/quizzes/<int:quiz_id>/edit", methods=["GET", "POST"])
@admin_required
@check_session_timeout
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuizAdminForm(obj=quiz)

    if form.validate_on_submit():
        quiz.title = form.title.data
        quiz.subject = form.subject.data
        quiz.quiz_type = form.quiz_type.data
        quiz.description = form.description.data
        db.session.commit()
        flash(f"Quiz '{quiz.title}' has been updated.", "success")
        return redirect(url_for('admin.quizzes'))

    if request.method == 'POST' and not form.validate():
        flash('Invalid form submission. Please check the errors below.', 'error')

    return render_template('admin/quiz_form.html', form=form, action='Edit', quiz=quiz)

@admin_bp.route("/quizzes/<int:quiz_id>/delete", methods=["POST"])
@admin_required
@check_session_timeout
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    flash("Quiz has been deleted.", "success")
    return redirect(url_for('admin.quizzes'))

@admin_bp.route("/quizzes/<int:quiz_id>/questions/add", methods=["GET", "POST"])
@admin_required
@check_session_timeout
def add_quiz_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionAdminForm()

    if form.validate_on_submit():
        question = QuizQuestion(
            quiz_id=quiz.id,
            question_text=form.question_text.data,
            option_a=form.option_a.data,
            option_b=form.option_b.data,
            option_c=form.option_c.data,
            option_d=form.option_d.data,
            correct_option=form.correct_option.data,
            explanation=form.explanation.data
        )
        db.session.add(question)
        db.session.commit()
        flash("Question added to quiz.", "success")
        return redirect(url_for('admin.quizzes'))

    if request.method == 'POST' and not form.validate():
        flash('Invalid form submission. Please check the errors below.', 'error')

    return render_template('admin/question_form.html', form=form, quiz=quiz)


@admin_bp.route("/quizzes/questions/<int:question_id>/delete", methods=["POST"])
@admin_required
@check_session_timeout
def delete_quiz_question(question_id):
    question = QuizQuestion.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash("Question deleted from quiz.", "success")
    return redirect(url_for('admin.quizzes'))

@admin_bp.route("/quizzes/<int:quiz_id>/questions/import", methods=["GET"])
@admin_required
def bulk_import_questions(quiz_id):
    """Show the bulk import page for a specific quiz."""
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('admin/bulk_import_questions.html', quiz=quiz)

@admin_bp.route("/quizzes/<int:quiz_id>/questions/import", methods=["POST"])
@admin_required
def process_bulk_import_questions(quiz_id):
    """Process the uploaded CSV file and import questions."""
    quiz = Quiz.query.get_or_404(quiz_id)

    if 'file' not in request.files:
        flash('No file selected.', 'error')
        return redirect(url_for('admin.bulk_import_questions', quiz_id=quiz.id))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('admin.bulk_import_questions', quiz_id=quiz.id))

    if not file.filename.endswith('.csv'):
        flash('Please upload a CSV file.', 'error')
        return redirect(url_for('admin.bulk_import_questions', quiz_id=quiz.id))

    try:
        content = file.read().decode('utf-8')
        import csv
        from io import StringIO
        reader = csv.DictReader(StringIO(content))
        added_count = 0
        for row in reader:
            if not all([row.get('question_text'), row.get('option_a'), row.get('option_b'),
                       row.get('option_c'), row.get('option_d'), row.get('correct_option')]):
                continue

            question = QuizQuestion(
                quiz_id=quiz.id,
                question_text=row['question_text'],
                option_a=row['option_a'],
                option_b=row['option_b'],
                option_c=row['option_c'],
                option_d=row['option_d'],
                correct_option=row['correct_option'].strip().lower(),
                explanation=row.get('explanation', '')
            )
            db.session.add(question)
            added_count += 1

        db.session.commit()
        flash(f'Successfully imported {added_count} questions from CSV.', 'success')

    except Exception as e:
        flash(f'Error importing CSV: {str(e)}', 'error')

    return redirect(url_for('admin.quizzes'))

@admin_bp.route("/quizzes/<int:quiz_id>/questions")
@admin_required
@check_session_timeout
def view_quiz_questions(quiz_id):
    """View all questions for a specific quiz."""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions.all()
    return render_template('admin/quiz_questions.html', quiz=quiz, questions=questions)

# VIDEO & PLAYLIST MANAGEMENT

@admin_bp.route("/videos")
@admin_required
@check_session_timeout
def videos():
    search = request.args.get('search', '')
    query = Playlist.query
    if search:
        query = query.filter(Playlist.title.ilike(f'%{search}%'))
    playlists = query.order_by(Playlist.title).all()
    return render_template('admin/videos.html', playlists=playlists, search=search)

@admin_bp.route("/videos/playlist/create", methods=["GET", "POST"])
@admin_required
@check_session_timeout
def create_playlist():
    form = PlaylistAdminForm()
    if form.validate_on_submit():
        playlist = Playlist(
            title=form.title.data,
            subject=form.subject.data,
            description=form.description.data,
            uploaded_by=current_user.id,
            status="approved",
        )
        db.session.add(playlist)
        db.session.commit()
        flash(f"Playlist '{playlist.title}' created.", "success")
        return redirect(url_for('admin.videos'))

    if request.method == 'POST' and not form.validate():
        flash('Invalid form submission. Please check the errors below.', 'error')

    return render_template('admin/playlist_form.html', form=form, action='Create')

@admin_bp.route("/videos/playlist/<int:playlist_id>/edit", methods=["GET", "POST"])
@admin_required
@check_session_timeout
def edit_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    form = PlaylistAdminForm(obj=playlist)
    if form.validate_on_submit():
        playlist.title = form.title.data
        playlist.subject = form.subject.data
        playlist.description = form.description.data
        db.session.commit()
        flash(f"Playlist '{playlist.title}' updated.", "success")
        return redirect(url_for('admin.videos'))

    if request.method == 'POST' and not form.validate():
        flash('Invalid form submission. Please check the errors below.', 'error')

    return render_template('admin/playlist_form.html', form=form, action='Edit', playlist=playlist)

@admin_bp.route("/videos/playlist/<int:playlist_id>/delete", methods=["POST"])
@admin_required
@check_session_timeout
def delete_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    db.session.delete(playlist)
    db.session.commit()
    flash("Playlist deleted.", "success")
    return redirect(url_for('admin.videos'))

@admin_bp.route("/videos/playlist/<int:playlist_id>/add", methods=["GET", "POST"])
@admin_required
@check_session_timeout
def add_video(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    form = VideoAdminForm()

    if form.validate_on_submit():
        video = Video(
            playlist_id=playlist.id,
            title=form.title.data,
            youtube_video_id=form.youtube_url.data,
            order_index=form.order_index.data,
            duration_seconds=form.duration_seconds.data
        )
        db.session.add(video)
        db.session.commit()
        flash(f"Video '{video.title}' added to playlist.", "success")
        return redirect(url_for('admin.videos'))

    return render_template('admin/video_form.html', form=form, playlist=playlist)

@admin_bp.route("/videos/<int:video_id>/delete", methods=["POST"])
@admin_required
@check_session_timeout
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    flash("Video deleted from playlist.", "success")
    return redirect(url_for('admin.videos'))

@admin_bp.route("/videos/playlist/<int:playlist_id>/import", methods=["GET", "POST"])
@admin_required
@check_session_timeout
def import_playlist_videos(playlist_id):
    """Import all videos from a YouTube playlist link."""
    playlist = Playlist.query.get_or_404(playlist_id)

    if request.method == "POST":
        playlist_url = request.form.get('playlist_url', '').strip()
        if not playlist_url:
            flash('Please enter a YouTube playlist URL.', 'error')
            return render_template('admin/playlist_import.html', playlist=playlist)

        playlist_id_from_url = extract_playlist_id(playlist_url)
        if not playlist_id_from_url:
            flash('Invalid YouTube playlist URL. Please check and try again.', 'error')
            return render_template('admin/playlist_import.html', playlist=playlist)

        try:
            videos_data = get_playlist_videos(playlist_id_from_url)
            if not videos_data:
                flash('No videos found in this playlist.', 'warning')
                return render_template('admin/playlist_import.html', playlist=playlist)

            added_count = 0
            for idx, video_data in enumerate(videos_data, start=1):
                existing = Video.query.filter_by(
                    playlist_id=playlist.id,
                    youtube_video_id=video_data['embed_url']
                ).first()
                if not existing:
                    video = Video(
                        playlist_id=playlist.id,
                        title=video_data['title'],
                        youtube_video_id=video_data['embed_url'],
                        order_index=idx,
                        duration_seconds=video_data['duration_seconds']
                    )
                    db.session.add(video)
                    added_count += 1

            db.session.commit()
            flash(f'Successfully imported {added_count} videos from the playlist.', 'success')
            return redirect(url_for('admin.videos'))

        except Exception as e:
            flash(f'Error fetching playlist: {str(e)}', 'error')
            return render_template('admin/playlist_import.html', playlist=playlist)

    return render_template('admin/playlist_import.html', playlist=playlist)

# MATERIALS MANAGEMENT

@admin_bp.route("/materials")
@admin_required
@check_session_timeout
def materials():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    status_filter = request.args.get('status', 'pending')

    query = Material.query
    if search:
        query = query.filter(Material.title.ilike(f'%{search}%'))
    if category:
        query = query.filter_by(category=category)
    if status_filter:
        query = query.filter_by(status=status_filter)

    materials = query.order_by(Material.uploaded_at.desc()).all()

    categories = db.session.query(Material.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]

    pending_count = Material.query.filter_by(status='pending').count()
    approved_count = Material.query.filter_by(status='approved').count()
    rejected_count = Material.query.filter_by(status='rejected').count()

    return render_template('admin/materials.html',
                           materials=materials,
                           categories=categories,
                           search=search,
                           category=category,
                           status_filter=status_filter,
                           pending_count=pending_count,
                           approved_count=approved_count,
                           rejected_count=rejected_count)

@admin_bp.route("/materials/<int:material_id>/delete", methods=["POST"])
@admin_required
@check_session_timeout
def delete_material(material_id):
    material = Material.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    flash(f"Material '{material.title}' deleted.", "success")
    return redirect(url_for('admin.materials'))

@admin_bp.route("/materials/add", methods=["GET", "POST"])
@admin_required
@check_session_timeout
def add_material():
    """Add a new study material (PDF or external link)."""
    form = MaterialUploadForm()

    if form.validate_on_submit():
        if form.file.data:
            relative_path = save_file(form.file.data, "materials")
            material = Material(
                uploaded_by=current_user.id,
                title=form.title.data,
                description=form.description.data,
                material_type="pdf",
                category=form.category.data,
                file_path=relative_path,
                subject=form.subject.data,
            )
        elif form.file_url.data:
            material = Material(
                uploaded_by=current_user.id,
                title=form.title.data,
                description=form.description.data,
                material_type="link",
                category=form.category.data,
                file_url=form.file_url.data,
                subject=form.subject.data,
            )
        else:
            flash("Please provide either a file or an external link.", "error")
            return render_template("admin/material_form.html", form=form)

        db.session.add(material)
        db.session.commit()
        flash(f"Material '{material.title}' added successfully.", "success")
        return redirect(url_for("admin.materials"))

    return render_template("admin/material_form.html", form=form)

@admin_bp.route("/materials/<int:material_id>/approve", methods=["POST"])
@admin_required
@check_session_timeout
def approve_material(material_id):
    material = Material.query.get_or_404(material_id)
    if material.status != 'pending':
        flash("This material has already been reviewed.", "warning")
        return redirect(url_for('admin.materials', status='pending'))
    material.status = 'approved'
    material.reviewed_by = current_user.id
    material.reviewed_at = datetime.utcnow()
    db.session.commit()
    flash(f"Material '{material.title}' approved.", "success")
    return redirect(url_for('admin.materials', status='pending'))

@admin_bp.route("/materials/<int:material_id>/reject", methods=["POST"])
@admin_required
@check_session_timeout
def reject_material(material_id):
    material = Material.query.get_or_404(material_id)
    if material.status != 'pending':
        flash("This material has already been reviewed.", "warning")
        return redirect(url_for('admin.materials', status='pending'))
    material.status = 'rejected'
    material.reviewed_by = current_user.id
    material.reviewed_at = datetime.utcnow()
    db.session.commit()
    flash(f"Material '{material.title}' rejected.", "success")
    return redirect(url_for('admin.materials', status='pending'))

# SETTINGS

@admin_bp.route("/settings")
@admin_required
@check_session_timeout
def settings():
    return render_template('admin/settings.html')
