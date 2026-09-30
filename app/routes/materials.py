from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.extensions import db
from app.models.material import Material
from app.models.paper import Paper
from app.models.video import Playlist
from app.forms.materials import MaterialUploadForm
from app.utils.decorators import profile_required
from app.utils.helpers import save_file

materials_bp = Blueprint("materials", __name__)


@materials_bp.route("/")
def list_materials():
    q = request.args.get("q", "").strip()
    subject = request.args.get("subject")
    category = request.args.get("category")

    query = Material.query.filter_by(status="approved").order_by(Material.uploaded_at.desc())
    if q:
        query = query.filter(or_(Material.title.ilike(f"%{q}%"), Material.subject.ilike(f"%{q}%")))
    if subject:
        query = query.filter_by(subject=subject)
    if category:
        query = query.filter_by(category=category)

    materials = query.all()
    return render_template("materials_list.html", materials=materials)


@materials_bp.route("/upload", methods=["GET", "POST"])
@login_required
@profile_required
def upload_material():
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
                status="pending",
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
                status="pending",
            )
        else:
            flash("Please provide either a file or an external link.", "error")
            return render_template("materials_upload.html", form=form)

        db.session.add(material)
        db.session.commit()
        flash("Material uploaded successfully! It will be visible after admin approval.", "success")
        return redirect(url_for("materials.my_uploads"))

    return render_template("materials_upload.html", form=form)


@materials_bp.route("/my-uploads")
@login_required
@profile_required
def my_uploads():
    """Show everything the current user has uploaded — with filter tabs."""
    filter_type = request.args.get("filter", "all")  # all | playlists | materials | papers

    materials = (
        Material.query
        .filter_by(uploaded_by=current_user.id)
        .order_by(Material.uploaded_at.desc())
        .all()
    )
    papers = (
        Paper.query
        .filter_by(uploaded_by=current_user.id)
        .order_by(Paper.uploaded_at.desc())
        .all()
    )
    playlists = (
        Playlist.query
        .filter_by(uploaded_by=current_user.id)
        .order_by(Playlist.created_at.desc())
        .all()
    )

    counts = {
        "all":       len(materials) + len(papers) + len(playlists),
        "materials": len(materials),
        "papers":    len(papers),
        "playlists": len(playlists),
    }

    return render_template(
        "materials_my_uploads.html",
        materials=materials,
        papers=papers,
        playlists=playlists,
        counts=counts,
        filter_type=filter_type,
    )
