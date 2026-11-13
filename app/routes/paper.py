import os
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request  # ✅ Added request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.paper import Paper
from app.forms.paper import UploadPaperForm
from app.utils.helpers import save_file
from sqlalchemy import or_

paper_bp = Blueprint("paper", __name__)

@paper_bp.route("/")
def list_papers():
    q = request.args.get("q", "").strip()
    exam_type = request.args.get("exam_type")

    query = Paper.query.filter_by(status="approved").order_by(Paper.uploaded_at.desc())
    if q:
        query = query.filter(or_(Paper.subject.ilike(f"%{q}%"), Paper.year.ilike(f"%{q}%")))
    if exam_type:
        query = query.filter_by(exam_type=exam_type)

    papers = query.all()
    return render_template("paper_list.html", papers=papers)

@paper_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    form = UploadPaperForm()

    if form.validate_on_submit():
        relative_path = save_file(form.file.data, "papers")

        paper = Paper(
            uploaded_by=current_user.id,
            subject=form.subject.data,
            exam_type=form.exam_type.data,
            year=form.year.data,
            file_path=relative_path,
            status="pending",
        )
        db.session.add(paper)
        db.session.commit()

        flash("Uploaded — pending admin approval.", "success")
        return redirect(url_for("paper.list_papers"))

    return render_template("paper_upload.html", form=form)
