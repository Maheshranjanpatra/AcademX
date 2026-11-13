from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.question import Question, Answer, Tag
from app.forms.qa import AskQuestionForm, AnswerForm
from app.utils.constants import POPULAR_TAGS, ALL_SUBJECTS
from app.utils.telegram import notify_question

qa_bp = Blueprint("qa", __name__)

@qa_bp.route("/")
def list_questions():
    subject = request.args.get("subject")
    query = Question.query.filter(Question.status != "rejected").order_by(
        Question.created_at.desc()
    )
    if subject:
        query = query.filter_by(subject=subject)
    questions = query.all()
    return render_template("qa_list.html", questions=questions, all_subjects=ALL_SUBJECTS)

@qa_bp.route("/ask", methods=["GET", "POST"])
@login_required
def ask():
    form = AskQuestionForm()

    if form.validate_on_submit():
        question = Question(
            user_id=current_user.id,
            title=form.title.data,
            body=form.body.data,
            subject=form.subject.data,
            is_anonymous=form.is_anonymous.data,
            status="approved",
        )

        tag_names = [t.strip() for t in (form.tags.data or "").split(",") if t.strip()]
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)
            question.tags.append(tag)

        db.session.add(question)
        db.session.commit()

        notify_question(
            asker=current_user.anonymous_id or current_user.username,
            title=question.title,
            body=question.body,
            link=url_for("admin.qa", _external=True),
        )
        flash("Question posted successfully.", "success")
        return redirect(url_for("qa.view_question", question_id=question.id))
    return render_template("qa_ask.html", form=form, popular_tags=POPULAR_TAGS)

@qa_bp.route("/<int:question_id>")
def view_question(question_id):
    question = Question.query.get_or_404(question_id)
    if question.status == "rejected":
        abort(404)
    answers = question.answers.order_by(Answer.upvotes.desc()).all()
    answer_form = AnswerForm()
    return render_template(
        "qa_detail.html", question=question, answers=answers, form=answer_form
    )

@qa_bp.route("/<int:question_id>/answer", methods=["POST"])
@login_required
def answer_question(question_id):
    question = Question.query.get_or_404(question_id)
    if question.status == "rejected":
        abort(404)

    form = AnswerForm()

    if form.validate_on_submit():
        answer = Answer(
            question_id=question.id,
            user_id=current_user.id,
            body=form.body.data,
            is_anonymous=form.is_anonymous.data,
        )
        db.session.add(answer)
        db.session.commit()
    else:
        flash("Answer cannot be empty.", "error")

    return redirect(url_for("qa.view_question", question_id=question_id))

@qa_bp.route("/<int:question_id>/upvote", methods=["POST"])
@login_required
def upvote_question(question_id):
    question = Question.query.get_or_404(question_id)
    if question.status == "rejected":
        abort(404)
    question.upvotes += 1
    db.session.commit()
    return redirect(url_for("qa.view_question", question_id=question_id))

@qa_bp.route("/answer/<int:answer_id>/best", methods=["POST"])
@login_required
def mark_best_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question = answer.question

    if question.user_id != current_user.id and not current_user.is_admin:
        flash("Only the question author or an admin can mark a best answer.", "error")
        return redirect(url_for("qa.view_question", question_id=question.id))

    for a in question.answers:
        a.is_best_answer = False
    answer.is_best_answer = True
    question.is_resolved = True
    db.session.commit()

    return redirect(url_for("qa.view_question", question_id=question.id))
