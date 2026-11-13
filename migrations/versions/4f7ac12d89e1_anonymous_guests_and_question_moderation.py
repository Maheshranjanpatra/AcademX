"""Replace personal user identifiers with pseudonymous guest profiles.

Revision ID: 4f7ac12d89e1
Revises: 2219be6d9dc2
Create Date: 2026-11-13
"""
import re
import secrets

from alembic import op
import sqlalchemy as sa


revision = "4f7ac12d89e1"
down_revision = "2219be6d9dc2"
branch_labels = None
depends_on = None


def _anonymize_users():
    bind = op.get_bind()
    bind.execute(sa.text("UPDATE users SET is_admin = FALSE WHERE is_admin IS NULL"))
    rows = bind.execute(
        sa.text("SELECT id, is_admin, anonymous_id FROM users ORDER BY id")
    ).mappings().all()
    guest_rows = [row for row in rows if not row["is_admin"]]
    if len(guest_rows) > 10_000:
        raise RuntimeError(
            "Cannot assign unique User_0000–User_9999 IDs to more than 10,000 guest profiles."
        )

    identities = {}
    invalid_rows = []
    for row in guest_rows:
        current_id = row["anonymous_id"] or ""
        if re.fullmatch(r"User_\d{4}", current_id):
            identities[row["id"]] = current_id
        else:
            invalid_rows.append(row)

    used = set(identities.values())
    available = [
        f"User_{number:04d}"
        for number in range(10_000)
        if f"User_{number:04d}" not in used
    ]
    if len(invalid_rows) > len(available):
        raise RuntimeError("No unused four-digit anonymous IDs remain.")
    secrets.SystemRandom().shuffle(available)

    for row, anonymous_id in zip(invalid_rows, available):
        identities[row["id"]] = anonymous_id

    for row in rows:
        if row["is_admin"]:
            identities[row["id"]] = (None, "Administrator")
            continue
        anonymous_id = identities[row["id"]]
        identities[row["id"]] = (anonymous_id, anonymous_id)

    for user_id, (anonymous_id, name) in identities.items():
        bind.execute(
            sa.text(
                "UPDATE users SET anonymous_id = :anonymous_id, name = :name WHERE id = :id"
            ),
            {"anonymous_id": anonymous_id, "name": name, "id": user_id},
        )


def upgrade():
    op.alter_column("users", "anonymous_id", existing_type=sa.String(length=20), nullable=True)
    op.get_bind().execute(sa.text("UPDATE users SET anonymous_id = NULL WHERE is_admin = TRUE"))
    _anonymize_users()

    bind = op.get_bind()
    inspector = sa.inspect(bind)
    for constraint in inspector.get_unique_constraints("users"):
        if set(constraint.get("column_names") or []) & {"google_sub", "email", "reg_num"}:
            op.drop_constraint(constraint["name"], "users", type_="unique")

    op.drop_column("users", "google_sub")
    op.drop_column("users", "email")
    op.drop_column("users", "reg_num")

    op.add_column(
        "questions",
        sa.Column("status", sa.String(length=20), nullable=False, server_default="approved"),
    )
    op.add_column("questions", sa.Column("reviewed_by", sa.Integer(), nullable=True))
    op.add_column("questions", sa.Column("reviewed_at", sa.DateTime(), nullable=True))
    op.create_foreign_key(
        "fk_questions_reviewed_by_users",
        "questions",
        "users",
        ["reviewed_by"],
        ["id"],
    )
    op.alter_column(
        "questions",
        "status",
        existing_type=sa.String(length=20),
        server_default="pending",
    )

    op.create_table(
        "admin_login_attempts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("address_hash", sa.String(length=64), nullable=False),
        sa.Column("attempted_at", sa.DateTime(), nullable=False),
    )
    op.create_index(
        "ix_admin_login_attempts_address_hash",
        "admin_login_attempts",
        ["address_hash"],
    )


def downgrade():
    op.drop_index("ix_admin_login_attempts_address_hash", table_name="admin_login_attempts")
    op.drop_table("admin_login_attempts")

    op.drop_constraint("fk_questions_reviewed_by_users", "questions", type_="foreignkey")
    op.drop_column("questions", "reviewed_at")
    op.drop_column("questions", "reviewed_by")
    op.drop_column("questions", "status")

    op.add_column("users", sa.Column("google_sub", sa.String(length=64), nullable=True))
    op.add_column("users", sa.Column("email", sa.String(length=120), nullable=True))
    op.add_column("users", sa.Column("reg_num", sa.String(length=40), nullable=True))
    op.create_unique_constraint("users_google_sub_key", "users", ["google_sub"])
    op.create_unique_constraint("users_email_key", "users", ["email"])
    op.create_unique_constraint("users_reg_num_key", "users", ["reg_num"])

    bind = op.get_bind()
    rows = bind.execute(
        sa.text("SELECT id, anonymous_id FROM users ORDER BY id")
    ).mappings().all()
    used = {row["anonymous_id"] for row in rows if row["anonymous_id"]}
    available = [
        f"User_{number:04d}"
        for number in range(10_000)
        if f"User_{number:04d}" not in used
    ]
    missing_ids = [row for row in rows if row["anonymous_id"] is None]
    if len(missing_ids) > len(available):
        raise RuntimeError("Cannot restore a non-null anonymous ID for every account.")
    secrets.SystemRandom().shuffle(available)
    for row, anonymous_id in zip(missing_ids, available):
        bind.execute(
            sa.text("UPDATE users SET anonymous_id = :anonymous_id WHERE id = :id"),
            {"anonymous_id": anonymous_id, "id": row["id"]},
        )

    op.alter_column("users", "anonymous_id", existing_type=sa.String(length=20), nullable=False)
