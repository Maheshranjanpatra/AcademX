from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.quiz import Quiz, QuizQuestion, QuizAttempt
from app.utils.decorators import profile_required

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/")
def list_quizzes():
    quizzes = Quiz.query.order_by(Quiz.created_at.desc()).all()
    return render_template("quiz_list.html", quizzes=quizzes)


@quiz_bp.route("/<int:quiz_id>/attempt", methods=["GET", "POST"])
@login_required
@profile_required
def attempt(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions.all()

    if request.method == "POST":
        score = 0
        responses = {}

        for q in questions:
            selected = request.form.get(f"question_{q.id}")
            responses[str(q.id)] = selected
            if selected == q.correct_option:
                score += 1

        attempt_record = QuizAttempt(
            quiz_id=quiz.id,
            user_id=current_user.id,
            score=score,
            total_questions=len(questions),
            responses=responses,
        )
        db.session.add(attempt_record)
        db.session.commit()

        return redirect(url_for("quiz.result", attempt_id=attempt_record.id))

    return render_template("quiz_attempt.html", quiz=quiz, questions=questions)


@quiz_bp.route("/result/<int:attempt_id>")
@login_required
@profile_required
def result(attempt_id):
    attempt_record = QuizAttempt.query.get_or_404(attempt_id)

    if attempt_record.user_id != current_user.id:
        flash("You can't view someone else's result.", "error")
        return redirect(url_for("quiz.list_quizzes"))

    questions = attempt_record.quiz.questions.all()
    return render_template("quiz_result.html", attempt=attempt_record, questions=questions)
